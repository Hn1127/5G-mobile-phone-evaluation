import json
import os
import pandas as pd

from snownlp import SnowNLP

#创建关键词列表
camerakeywords=[]
appearancekeywords=[]
batterykeywords=[]
pricekeywords=[]
performancekeywords=[]

#此处输入路径
splitcommentpath=r'./splitcomment/'
scorepath=r'./score/'
#此处输入csv文件路径
#phoneinfo=pd.read_csv(r'phone_info_jd.csv')

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
        with open(scorepath+file.split('.')[0]+".txt",'w',encoding='utf-8') as f:
            f.write("相机评分："+str(camerascore)+'\n')
            f.write("电池评分："+str(batteryscore)+'\n')
            f.write("外观评分：" + str(appearancescore) + '\n')
            f.write("性能评分：" + str(performancescore) + '\n')
            f.write("价格评分：" + str(pricescore) + '\n')
