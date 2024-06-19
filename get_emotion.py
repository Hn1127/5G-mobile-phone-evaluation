import json
import os
import pandas as pd
import numpy as np

from snownlp import SnowNLP

#创建关键词列表
camerakeywords=[]
appearancekeywords=[]
batterykeywords=[]
pricekeywords=[]
performancekeywords=[]
servicekeywords=[]

checklist=np.arange(52)

#此处输入路径
splitcommentpath=r'./splitcomment/'
scorepath=r'./score/'
#此处输入csv文件路径
p=np.array(pd.read_csv(r'phone_info_jd.csv'))
phoneinfo=p.tolist()


#读入关键词
def readkeywords():
    f=open(r'./camerakeywords.txt',encoding='utf-8')
    for line in f:
        camerakeywords.append(line.strip('\n'))
    f=open(r'./appearancekeywords.txt',encoding='utf-8')
    for line in f:
        appearancekeywords.append(line.strip('\n'))
    f=open(r'./performancekeywords.txt',encoding='utf-8')
    for line in f:
        performancekeywords.append(line.strip('\n'))
    f=open(r'./batterykeywords.txt',encoding='utf-8')
    for line in f:
        batterykeywords.append(line.strip('\n'))
    f=open(r'./pricekeywords.txt',encoding='utf-8')
    for line in f:
        pricekeywords.append(line.strip('\n'))
    f = open(r'./servicekeywords.txt', encoding='utf-8')
    for line in f:
        servicekeywords.append(line.strip('\n'))

#判断一条评论中是否含有关键词
def contain(comment:str,wordlist:list)->bool:
    for word in wordlist:
        if comment.find(word)!=-1:
            return True
    return False

#读取评论
def getscore(filepath:str,keywordlist:list)->float:
        #full_points标记评分满分
        full_points=10.
        comment_number=0
        emotion=0.
        f = open(filepath, 'r', encoding='utf-8')
        segments=json.load(f)
        for record in segments['split_comments']:
            if contain(record,keywordlist):
                comment_number+=1
                emotion+=SnowNLP(record).sentiments
        return full_points*emotion/comment_number


if __name__=="__main__":
    readkeywords()
    files=os.listdir(splitcommentpath)
    for file in files:
        camerascore=getscore(splitcommentpath+file,camerakeywords)
        batteryscore=getscore(splitcommentpath+file,batterykeywords)
        appearancescore=getscore(splitcommentpath+file,appearancekeywords)
        performancescore=getscore(splitcommentpath+file,performancekeywords)
        pricescore=getscore(splitcommentpath+file,pricekeywords)
        servicescore=getscore(splitcommentpath+file,servicekeywords)
        with open(scorepath+file.split('.')[0]+".txt",'w',encoding='utf-8') as f:
            i=0
            for line in phoneinfo:
                if str(line[0])==file.split('.')[0]:
                    f.write("品牌："+line[1]+'\n')
                    f.write("型号："+line[2]+'\n')
                    f.write("售价："+line[3]+'\n')
                    checklist[i]=-1
                    break
                i+=1
            f.write("相机评分："+str(camerascore)+'\n')
            f.write("电池评分："+str(batteryscore)+'\n')
            f.write("外观评分：" + str(appearancescore) + '\n')
            f.write("性能评分：" + str(performancescore) + '\n')
            f.write("性价比评分：" + str(pricescore) + '\n')
            f.write("商家服务评分："+str(servicescore)+'\n')

'''
100088850072 100081538612 两组数据在csv中找不到对应的手机信息
csv件中有两行重复
检查数组第22行（对应csv第23行，与第22行重复） 第52行（对应csv文件缺失的一行）出现问题
手机信息中只有51条记录 但评论有52个文件
'''
