import csv
import os

import numpy as np

phone=[]

filelist=os.listdir(r'./score')
listdir=r'./score/'
rankdir=r'./rank/'
keys=["品牌","型号","售价","相机评分","电池评分","外观评分","性能评分","性价比评分","商家服务评分"]


for file in filelist:
    f=open(listdir+file,'r',encoding='utf-8')
    strings =f.readlines()
    values=[]
    for s in  strings:
        values.append(s.split('：')[1].strip('\n'))
    a=dict(zip(keys,values))
    phone.append(a)

rank1=sorted(phone,key=lambda s:s["相机评分"],reverse=True)
rank2=sorted(phone,key=lambda s:s["电池评分"],reverse=True)
rank3=sorted(phone,key=lambda s:s["外观评分"],reverse=True)
rank4=sorted(phone,key=lambda s:s["性能评分"],reverse=True)
rank5=sorted(phone,key=lambda s:s["性价比评分"],reverse=True)
rank6=sorted(phone,key=lambda s:s["商家服务评分"],reverse=True)

#形成txt格式的排行榜
'''
f=open(rankdir+"camera_rank.txt",'w',encoding='utf-8')
f.write("相机排行榜"+'\n')
i=1
for element in rank1:
   f.write(str(i)+' '+element["品牌"]+' '+element["型号"]+' '+element["相机评分"]+'\n')
   i+=1

f=open(rankdir+"battery_rank.txt",'w',encoding='utf-8')
f.write("电池排行榜"+'\n')
i=1
for element in rank2:
   f.write(str(i)+' '+element["品牌"]+' '+element["型号"]+' '+element["电池评分"]+'\n')
   i+=1

f=open(rankdir+"appearance_rank.txt",'w',encoding='utf-8')
f.write("外观排行榜"+'\n')
i=1
for element in rank3:
   f.write(str(i)+' '+element["品牌"]+' '+element["型号"]+' '+element["外观评分"]+'\n')
   i+=1

f=open(rankdir+"performance_rank.txt",'w',encoding='utf-8')
f.write("性能排行榜"+'\n')
i=1
for element in rank4:
   f.write(str(i)+' '+element["品牌"]+' '+element["型号"]+' '+element["性能评分"]+'\n')
   i+=1

f=open(rankdir+"price_rank.txt",'w',encoding='utf-8')
f.write("性价比排行榜"+'\n')
i=1
for element in rank5:
   f.write(str(i)+' '+element["品牌"]+' '+element["型号"]+' '+element["性价比评分"]+'\n')
   i+=1

f=open(rankdir+"service_rank.txt",'w',encoding='utf-8')
f.write("商家服务评分排行榜"+'\n')
i=1
for element in rank6:
   f.write(str(i)+' '+element["品牌"]+' '+element["型号"]+' '+element["商家服务评分"]+'\n')
   i+=1
'''
#形成csv格式的排行榜

with open(rankdir+"camera_rank.csv",'w',encoding='utf-8',newline="") as csvfile:
    head=['排名','品牌','型号','相机评分']
    writer=csv.DictWriter(csvfile,fieldnames=head)
    i=1
    writer.writeheader()
    for element in rank1:
        writer.writerow({'排名':str(i),'品牌':element["品牌"],'型号':element["型号"],'相机评分':element["相机评分"]})
        i+=1

with open(rankdir+"battery_rank.csv",'w',encoding='utf-8',newline="") as csvfile:
    head=['排名','品牌','型号','电池评分']
    writer=csv.DictWriter(csvfile,fieldnames=head)
    i=1
    writer.writeheader()
    for element in rank2:
        writer.writerow({'排名':str(i),'品牌':element["品牌"],'型号':element["型号"],'电池评分':element["电池评分"]})
        i+=1

with open(rankdir+"appearance_rank.csv",'w',encoding='utf-8',newline="") as csvfile:
    head=['排名','品牌','型号','外观评分']
    writer=csv.DictWriter(csvfile,fieldnames=head)
    i=1
    writer.writeheader()
    for element in rank3:
        writer.writerow({'排名':str(i),'品牌':element["品牌"],'型号':element["型号"],'外观评分':element["外观评分"]})
        i+=1

with open(rankdir+"performance_rank.csv",'w',encoding='utf-8',newline="") as csvfile:
    head=['排名','品牌','型号','性能评分']
    writer=csv.DictWriter(csvfile,fieldnames=head)
    i=1
    writer.writeheader()
    for element in rank4:
        writer.writerow({'排名':str(i),'品牌':element["品牌"],'型号':element["型号"],'性能评分':element["性能评分"]})
        i+=1

with open(rankdir+"price_rank.csv",'w',encoding='utf-8',newline="") as csvfile:
    head=['排名','品牌','型号','性价比评分']
    writer=csv.DictWriter(csvfile,fieldnames=head)
    i=1
    writer.writeheader()
    for element in rank5:
        writer.writerow({'排名':str(i),'品牌':element["品牌"],'型号':element["型号"],'性价比评分':element["性价比评分"]})
        i+=1

with open(rankdir+"service_rank.csv",'w',encoding='utf-8',newline="") as csvfile:
    head=['排名','品牌','型号','商家服务评分']
    writer=csv.DictWriter(csvfile,fieldnames=head)
    i=1
    writer.writeheader()
    for element in rank6:
        writer.writerow({'排名':str(i),'品牌':element["品牌"],'型号':element["型号"],'商家服务评分':element["商家服务评分"]})
        i+=1

