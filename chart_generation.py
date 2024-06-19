import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import MultipleLocator
import numpy as np
import os
import pygal   

phone=pd.read_csv('D:\spider(爬虫)\数据处理\\5G-mobile-phone-evaluation-main\data_prepare\phone_info_jd.csv')
index=['相机评分','电池评分','外观评分','性能评分','性价比评分','商家服务评分']
#此处输入存放分数指标文件的目录路径
scorepath='./score/'
#此处输入存放雷迖图的目录路径
rabar_chart_path='./rabar_chart/'
bar_chart_path='./bar_chart/'

def ID_mappping(keyword)->dict:
    '''
        keyword:輸入需要去重的标签，比如:品牌
        返回一个字典,字典的key是keyword,value是属于对应品牌的所有商品的ID
    '''
    duplicates_list=phone[keyword].drop_duplicates().to_list()
    empty_list=[[] for _ in duplicates_list]
    duplicates_dict=dict(zip(duplicates_list,empty_list))
    for key in duplicates_dict:
        duplicates_dict[key]=phone[phone[keyword]==key]['ID'].to_list()
    return duplicates_dict

def get_avg(keyword):
    '''
        得到对应keyword的手机的评分平均值
    '''
    band_dict=ID_mappping(keyword)
    scorepath='./score/'
    index=['相机评分','电池评分','外观评分','性能评分','性价比评分','商家服务评分']
    df=pd.DataFrame(index=index)
    for name,value in band_dict.items():
        elements=np.zeros(len(index))
        for v in value:
            element=[]
            with open(scorepath+str(v)+'.txt','r',encoding='utf-8') as f:
                element=[float(i.split('\n')[0].split('：')[-1]) for i in f.readlines()[3:]]
                elements=elements+np.array(element)
        df[name]=(elements/len(value)).tolist()
    return df

    
def radar_chart_single(): 
    ''' 
        生成每款手机的雷迖图
    ''' 
    df=get_avg('品名')
    for phone in df.columns.to_list():
        chart=pygal.Radar()
        chart.x_labels=index
        chart.title=phone
        chart.add('score',df[phone].values)
        chart.range=[0,10]
        chart.render_to_file(rabar_chart_path+phone.strip()+'.svg')

def rabar_chart_band():
    ''' 
        生成各品牌对比的雷迖图
    '''
    df=get_avg('品牌')
    chart=pygal.Radar()
    chart.x_labels=index
    chart.title='各品牌性能对比'
    for band in df.columns.to_list():
        chart.add(band,df[band].values)
    chart.range=[0,10]
    chart.render_to_file(rabar_chart_path+'rabar_chart_band.svg')

def rank_chart():
    ''' 
        生成各性能指标的排行
    '''
    appearance_band,appearance_score=pd.read_csv('./appearance_rank.csv')['型号'],pd.read_csv('./appearance_rank.csv')['外观评分']
    battery_band,battery_score=pd.read_csv('./battery_rank.csv')['型号'],pd.read_csv('./battery_rank.csv')['电池评分']
    camera_band,camera_score=pd.read_csv('./camera_rank.csv')['型号'],pd.read_csv('./camera_rank.csv')['相机评分']
    performance_band,performance_score=pd.read_csv('./performance_rank.csv')['型号'],pd.read_csv('./performance_rank.csv')['性能评分']
    price_band,price_score=pd.read_csv('./price_rank.csv')['型号'],pd.read_csv('./price_rank.csv')['性价比评分']
    service_band,service_score=pd.read_csv('./service_rank.csv')['型号'],pd.read_csv('./service_rank.csv')['商家服务评分']
    
    appearance_chart=pygal.HorizontalBar()
    appearance_chart.title='手机外观排行'
    appearance_chart.add('评分',appearance_score.to_list()[::-1])
    appearance_chart.x_labels=appearance_band.to_list()[::-1]
    appearance_chart.render_to_file(bar_chart_path+'appearance_chart.svg')

    battery_chart=pygal.HorizontalBar()
    battery_chart.title='手机电池性能排行'
    battery_chart.add('评分',battery_score.to_list()[::-1])
    battery_chart.x_labels=battery_band.to_list()[::-1]
    battery_chart.render_to_file(bar_chart_path+'battery_chart.svg')

    camera_chart=pygal.HorizontalBar()
    camera_chart.title='手机相机排行'
    camera_chart.add('评分', camera_score.to_list()[::-1])
    camera_chart.x_labels=camera_band.to_list()[::-1]
    camera_chart.render_to_file(bar_chart_path+'camera_chart.svg')

    performance_chart=pygal.HorizontalBar()
    performance_chart.title='手机性能排行'
    performance_chart.add('评分', performance_score.to_list()[::-1])
    performance_chart.x_labels=performance_band.to_list()[::-1]
    performance_chart.render_to_file(bar_chart_path+'performance_chart.svg')

    price_chart=pygal.HorizontalBar()
    price_chart.title='手机性价比排行'
    price_chart.add('评分', price_score.to_list()[::-1])
    price_chart.x_labels=price_band.to_list()[::-1]
    price_chart.render_to_file(bar_chart_path+'price_chart.svg')

    service_chart=pygal.HorizontalBar()
    service_chart.title='手机性价比排行'
    service_chart.add('评分', service_score.to_list()[::-1])
    service_chart.x_labels=service_band.to_list()[::-1]
    service_chart.render_to_file(bar_chart_path+'service_chart.svg')

    
if __name__=='__main__':
    if not os.path.exists(rabar_chart_path):
        os.mkdir(rabar_chart_path)
    if not os.path.exists(bar_chart_path):
        os.mkdir(bar_chart_path)
    radar_chart_single()
    rabar_chart_band()
    rank_chart()






