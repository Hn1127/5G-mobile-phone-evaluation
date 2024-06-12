import json
import os
import re

#此处输入路径
commentpath=r'./comment/'
splitcommentpath=r'splitcomment/'

#读取文件并拆分
#comment：原始评论（dict）
#segment：List 每个元素为评论小段
#评论使用。！ ？ \n \r \t拆分 并自动排除空段
files =os.listdir(commentpath)
for file in files:
    f=open(commentpath+file,'r',encoding='utf-8_sig')
    comment=json.load(f)
    segment=[]
    for singlecomment in comment["good_comments"]:
        list_comments=re.split('。|！|？|\n|\r|\t',singlecomment)
        for list in list_comments:
            if list!=""and list!="此用户未填写评价内容":
             segment.append(list)
    for singlecomment in comment["mid_comments"]:
        list_comments=re.split('。|！|？|\n|\r|\t',singlecomment)
        for list in list_comments:
            if list != ""and list!="此用户未填写评价内容":
                segment.append(list)
    for singlecomment in comment["bad_comments"]:
        list_comments=re.split('。|！|？|\n|\r|\t',singlecomment)
        for list in list_comments:
            if list != "" and list!="此用户未填写评价内容" :
                segment.append(list)
    with open(splitcommentpath+file,'w',encoding='utf-8') as f1:
        phone_comment = {
            'split_comments': segment,
        }
        f1.write(json.dumps(phone_comment, ensure_ascii=False, indent=4))