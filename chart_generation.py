import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import MultipleLocator
import numpy as np
import os
import pygal   

phone=pd.read_csv('D:\spider(爬虫)\数据处理\\5G-mobile-phone-evaluation-main\data_prepare\phone_info_jd.csv')
index=['相机评分','电池评分','外观评分','性能评分','价格评分','商家服务评分']
#此处输入存放分数指标文件的目录路径
scorepath='./score/'
#此处输入存放雷迖图的目录路径
chartpath='./rabar_chart/'

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
    index=['相机评分','电池评分','外观评分','性能评分','价格评分','商家服务评分']
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
        chart.render_to_file(chartpath+phone.strip()+'.svg')

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
    chart.render_to_file(chartpath+'rabar_chart_band.svg')

    

if __name__=='__main__':
    if not os.path.exists(chartpath):
        os.mkdir(chartpath)
    radar_chart_single()
    rabar_chart_band()






