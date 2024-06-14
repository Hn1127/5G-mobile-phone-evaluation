import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import MultipleLocator
import numpy as np
import os
import pygal   

phone=pd.read_csv('D:\spider(爬虫)\数据处理\\5G-mobile-phone-evaluation-main\data_prepare\phone_info_jd.csv')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
index=['相机评分','电池评分','外观评分','性能评分','价格评分','商家服务评分']
#此处输入存放分数指标文件的目录路径
scorepath='./score/'
#此处输入存放雷迖图的目录路径
chartpath='./rabar_chart/'

def ID_mappping()->dict:
    '''
        返回一个字典,字典的key是品牌名稱,value是属于对应品牌的所有商品的ID
    '''
    band_list=phone['品牌'].drop_duplicates().to_list()
    empty_list=[[] for _ in band_list]
    name_dict=dict(zip(band_list,empty_list))
    for name in name_dict:
        name_dict[name]=phone[phone['品牌']==name]['ID'].to_list()
    return name_dict

def get_avg():
    '''
        得到各个品牌的评分平均值
    '''
    band_dict=ID_mappping()
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
    
def radar_chart_single(datapath): 
    ''' 
        生成每款手机的雷迖图
    ''' 
    ID=datapath.split('/')[-1].split('.')[0]
    with open(datapath,'r',encoding='utf-8') as f:
        line=f.read().split('\n')
        phone_name=line[1].split('：')[-1]
        line=line[3:-1]
    data=[ float(d.split('：')[-1]) for d in line]
    chart=pygal.Radar()
    chart.x_labels=index
    chart.title=phone_name
    chart.add('score',data)
    chart.range=[0,10]
    chart.render_to_file(chartpath+ID+'.svg')

def rabar_chart_band():
    ''' 
        生成各品牌对比的雷迖图
    '''
    df=get_avg()
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
    files=os.listdir(scorepath)
    for file in files:
        radar_chart_single(scorepath+file)
    rabar_chart_band()






