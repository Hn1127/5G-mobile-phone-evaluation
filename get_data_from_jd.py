import time
import re
import csv
import json
import traceback
import winsound

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

psorts = {
    '销量': 3,
    '评论数': 4
}

MaxPages = 10
MaxProductName = 100
MaxCommentNum = 30
psort = psorts['销量']
KeyWord = '5g手机'

comment_dirname = 'comment'
phone_info_jd_filepath = 'phone_info_jd.csv'
id_map = []
try:
    id_map = pd.read_csv(phone_info_jd_filepath)['ID'].values.tolist()
except:
    id_map = []


def get_data(phone_info_jd_filepath, key="5g手机", max_pages=1, max_product_num=10, psort=3, max_comment_num=20):
    # 使用Chrome浏览器驱动程序
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    with open('stealth.min.js', 'r') as f:
        js = f.read()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})
    # 登录京东并获取cookie
    driver.get("https://passport.jd.com/new/login.aspx?/")
    cookie_file = 'cookie.txt'

    def login():
        # 判断是否有 cookie.txt 文件
        if os.path.exists(cookie_file):
            # 读取cookie文件中的内容
            driver.get(f"https://www.jd.com/")
            time.sleep(2)
            with open(cookie_file, 'r') as file:
                # 读取文件中的 cookie
                cookies = json.load(file)
                # 加载cookie信息
                for cookie in cookies:
                    driver.add_cookie(cookie)
            print('使用已保存的cookie登录')
        else:
            driver.get("https://passport.jd.com/new/login.aspx?/")
            # 等待用户登录并获取cookie
            time.sleep(10)  # 第一次使用需要用户手动登录获取cookie,可根据网络状况修改
            dictcookies = driver.get_cookies()
            jsoncookies = json.dumps(dictcookies)
            with open('cookie.txt', 'w') as f:
                f.write(jsoncookies)
            print('cookies已保存')

    try:
        login()
    except:
        print('登录出错!')

    # 发送请求获得搜索内容
    url = f"https://search.jd.com/Search?keyword={key}&psort={psort}"
    driver.get(url)

    # 初始化变量
    page_number = 1
    product_num = 0
    data = []

    # 爬取当前页面每一项数据
    while page_number <= max_pages:
        print("正在爬取第", page_number, "页")

        # 使用BeautifulSoup解析html内容
        html_parse = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(2)
        # 查找所有包含产品信息的class为“gl-i-wrap”的div
        div_list = html_parse.find_all("div", class_="gl-i-wrap")

        # 从每个div中提取文本信息
        # 每一个div是一个商品项
        for div in div_list:
            # 商品名、价格、评价数
            name = div.find("div", class_="p-name").get_text().strip().replace("\n", "")  # 商品宣传名
            try:
                price = div.find("div", class_="p-price").get_text().strip()
                if price == '￥':
                    price = '暂无参考价'
                comment_count = div.find("div", class_="p-commit")
                comment_count = comment_count.find("strong").get_text().strip()
                comment_count = comment_count.replace('条评价', '').replace('+', '')
                if '万' in comment_count:
                    comment_count = float(comment_count.replace('万', '')) * 10000
                comment_count = int(comment_count)
                # 获取商品详情页链接
                link = div.find("div", class_="p-name").find("a").get("href")
                id = link.replace("//item.jd.com/", "").replace(".html", "")
                if int(id) in id_map:
                    print(f'{name}已经爬取过')
                    continue
                if "http" not in link:
                    link = "https:" + link
            except:
                print(f'error1:在爬取{name}:{driver.current_url}时出错:获取详情页链接错误')
            try:
                # 打开新标签页, 商品详情页
                driver.execute_script(f'''window.open("{link}","_blank");''')
                # 切换到新标签页
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                # 等待2秒等待加载完毕
                time.sleep(2)
                # 解析html页面
                html_parse_new = BeautifulSoup(driver.page_source, "html.parser")
            except:
                print(f'error2:在爬取{name}:{driver.current_url}时出错:跳转详情页错误')
            try:
                # 获取商品品牌、正规品名以及对应价格
                brand = html_parse_new.find("a", clstag="shangpin|keycount|product|pinpai_1").get_text().strip()
                name = html_parse_new.find("li", string=re.compile("商品名称")).get_text().replace('商品名称：',
                                                                                                   '').strip()
                # 查看商品评价
                tab_menu = driver.find_elements_by_css_selector('#detail > div.tab-main.large > ul > li')
                for i, btn in enumerate(tab_menu):
                    if "商品评价" in btn.text:
                        btn.click()
                        break
                time.sleep(1)
                # 获取好评率
                good_comment_percent = driver.find_element_by_css_selector(
                    '#comment > div.mc > div.comment-info.J-comment-info > div.comment-percent > div').text
                # 获取评论关键字
                comment_tags = driver.find_elements_by_css_selector(
                    '#comment > div.mc > div.comment-info.J-comment-info > div.percent-info > div > span')
                tags = []
                for i, tag in enumerate(comment_tags):
                    tags.append(tag.text)
                # 将商品添加到列表中
                info = {
                    'ID': id,
                    '品牌': brand,
                    '品名': name,
                    '价格': price,
                    '评论数': comment_count,
                    '好评率': good_comment_percent,
                    '关键字': tags
                }
                # 打印商品信息
                print(info)
                data.append(info)
                save_data([info])
            except:
                time.sleep(3)
                print(f'error3:在爬取{name}:{driver.current_url}基本信息时出错')
            finally:
                # 关闭当前页面，返回搜索页
                driver.close()
                driver.switch_to.window(windows[0])
            product_num += 1
            print(f'------------------------{product_num}/{max_product_num}------------------------')
            if product_num >= max_product_num:
                break
        # 点击下一页按钮（如果可用）
        next_page_button = driver.find_element_by_class_name("pn-next")
        if next_page_button:
            next_page_button.click()
            time.sleep(3)  # 延迟以完全加载下一页
        else:
            break
        page_number += 1
    return data


def get_comments(max_comment_num):
    # 使用Chrome浏览器驱动程序
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    with open('stealth.min.js', 'r') as f:
        js = f.read()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})
    # 登录京东并获取cookie
    driver.get("https://passport.jd.com/new/login.aspx?/")
    cookie_file = 'cookie.txt'

    def login():
        # 判断是否有 cookie.txt 文件
        if os.path.exists(cookie_file):
            # 读取cookie文件中的内容
            driver.get(f"https://www.jd.com/")
            time.sleep(2)
            with open(cookie_file, 'r') as file:
                # 读取文件中的 cookie
                cookies = json.load(file)
                # 加载cookie信息
                for cookie in cookies:
                    driver.add_cookie(cookie)
            print('使用已保存的cookie登录')
        else:
            driver.get("https://passport.jd.com/new/login.aspx?/")
            # 等待用户登录并获取cookie
            time.sleep(10)  # 第一次使用需要用户手动登录获取cookie,可根据网络状况修改
            dictcookies = driver.get_cookies()
            jsoncookies = json.dumps(dictcookies)
            with open('cookie.txt', 'w') as f:
                f.write(jsoncookies)
            print('cookies已保存')

    try:
        login()
    except:
        print('登录出错!')

    # 根据cvs文件内容读取评论
    id_list = pd.read_csv(phone_info_jd_filepath)['ID'].values.tolist()

    # 搜索评论
    def get_comment_score(score):
        comments = []
        comment_page = 0
        comment_num = 0
        pageSize = 30
        while comment_num < max_comment_num:
            try:
                comment_json_url = (
                    "https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&"
                    "client=pc&clientVersion=1.0.0&"
                    f"body={{productId:{id},score:{score},sortType:5,page:{comment_page},pageSize:{pageSize}}}")

                time.sleep(8)
                windows = driver.window_handles
                driver.execute_script(f'''window.open("{comment_json_url}","_blank");''')
                comment_page += 1
                comment_num += pageSize
                # 切换到新标签页
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                time.sleep(1)
                # 记录数据
                comment_json_html = driver.find_elements_by_css_selector('body > pre')[0].text
                comment_json = json.loads(comment_json_html)
                comments_item = comment_json["comments"]
                comments.extend([comment["content"] for comment in comments_item])
            except:
                comments = []
                res = driver.find_elements_by_css_selector('body > pre')[0].text
                res_json = json.loads(res)
                if res_json["code"] == "605":
                    winsound.Beep(1000, 1000)
                    print('验证问题')
                    time.sleep(10)
                print(f'爬取{id}时出错')
            finally:
                # 关闭当前页面
                driver.close()
                driver.switch_to.window(windows[0])
        return comments

    for id in id_list:
        try:
            # 若该文件已经存在则不爬取
            if os.path.exists(f"{comment_dirname}/{id}.json"):
                print(f'{comment_dirname}/{id}.json 已存在')
                continue
            good_comments = get_comment_score(3)
            print(f'{id}好评爬取完毕，数量{max_comment_num}')
            mid_comments = get_comment_score(2)
            print(f'{id}中评爬取完毕，数量{max_comment_num}')
            bad_comments = get_comment_score(1)
            print(f'{id}差评爬取完毕，数量{max_comment_num}')
            with open(f"{comment_dirname}/{id}.json", "w", encoding="utf-8_sig") as f:
                phone_comment = {
                    'good_comments': good_comments,
                    'mid_comments': mid_comments,
                    'bad_comments': bad_comments
                }
                f.write(json.dumps(phone_comment, ensure_ascii=False, indent=4))
                print(f'评论写入 {comment_dirname}/{id}.json')
        except:
            print(f'{id}评论爬取出错')
            continue


def save_data(data):
    # 将数据保存到CSV文件中
    fields = ["ID", "品牌", "品名", "价格", "评论数", "好评率", "关键字"]

    with open(phone_info_jd_filepath, 'a', newline='', encoding='utf_8_sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerows(data)

    print("数据已保存到", phone_info_jd_filepath)


if __name__ == "__main__":
    data = get_data(phone_info_jd_filepath, KeyWord, MaxPages, MaxProductName, psort, MaxCommentNum)
    get_comments(MaxCommentNum)
