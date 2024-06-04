import time
import re
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

KeyWord = '5g手机'
MaxPages = 1
MaxProductName = 10


def get_data(key="5g手机", max_pages=1, max_product_num=10):
    # 使用Chrome浏览器驱动程序
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 登录并获取cookie
    # 京东网页的登录界面
    driver.get("https://passport.jd.com/new/login.aspx?/")
    cookie_file = 'cookie.txt'
    try:
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
    except:
        print('登录出错!')
        exit(0)

    # 发送请求获得搜索内容
    url = f"https://search.jd.com/Search?keyword={key}"
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
                commit = div.find("div", class_="p-commit").get_text().strip()
                commit = commit.replace('条评价', '').replace('+', '')
                if '万' in commit:
                    commit = float(commit.replace('万', '')) * 10000
                commit = int(commit)

                # 获取商品详情页链接
                link = div.find("div", class_="p-name").find("a").get("href")
                if "http" not in link:
                    link = "https:" + link

                # 打开新标签页, 商品详情页
                driver.execute_script(f'''window.open("{link}","_blank");''')
                # 切换到新标签页
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                # 等待3秒等待加载完毕
                time.sleep(3)
                # 解析html页面
                html_parse_new = BeautifulSoup(driver.page_source, "html.parser")
                time.sleep(1)

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
                good_commit_percent = driver.find_element_by_css_selector(
                    '#comment > div.mc > div.comment-info.J-comment-info > div.comment-percent > div').text
                # 获取评论关键字
                commit_tags = driver.find_elements_by_css_selector(
                    '#comment > div.mc > div.comment-info.J-comment-info > div.percent-info > div > span')
                tags = []
                for i, tag in enumerate(commit_tags):
                    tags.append(tag.text)

                # 将商品添加到列表中
                info = {
                    '品牌': brand,
                    '品名': name,
                    '价格': price,
                    '评论数': commit,
                    '好评率': good_commit_percent,
                    '关键字': tags
                }
                data.append(info)
                # 搜索评论
                # 关闭当前页面，返回搜索页
                driver.close()
                driver.switch_to.window(windows[0])
                # 打印商品信息
                print(info)
            except:
                print(f'在爬取{name}:{driver.current_url}时出错')
            product_num += 1
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
    # 关闭浏览器驱动程序
    driver.quit()
    return data


def save_data(data):
    # 将数据保存到CSV文件中
    filename = "phone_info_jd.csv"
    fields = ["品牌", "品名", "价格", "评论数", "好评率", "关键字"]

    with open(filename, 'w', newline='', encoding='utf_8_sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    print("数据已保存到", filename)


if __name__ == "__main__":
    data = get_data(KeyWord, MaxPages, MaxProductName)
    save_data(data)
