# -*- coding:utf-8 -*-
# import jieba
import json
import re
import csv
# from jieba import analyse
import math
import datetime

class Info_Struct:
    #包括网址，发布日期，题目，正文内容，转发者名字，信息来源名字（如果有的话），关键字
    def __init__(self, ID, release_Date, title, text, forward_Name, source_Name,
                 attitudes_count, comments_count, keywords):
        self.ID = ID
        # self.url = url
        self.release_Date = release_Date
        self.title = title
        self.text = text
        self.forward_Name = forward_Name
        self.source_Name = source_Name
        self.attitudes_count = attitudes_count
        self.comments_count = comments_count
        self.keywords = keywords

def timeChange(date_time):
    '''
    change the date_time format(20170625073800) to datetime's format(2017-06-25 07:38:00)
    :param date_time: string   the format is like 20170625073800
    :return: change_result: datetime
    '''
    # print(date_time)
    year = int(date_time[0:4])
    # print(year)
    month = int(date_time[4:6])
    day = int(date_time[6:8])
    hour = int(date_time[8:10])
    minute = int(date_time[10:12])
    second = int(date_time[12:14])
    result = datetime.datetime(year, month, day, hour, minute, second)
    return result

#匹配模式/xx网、xx社、xx报
p1 = ".*?[网社报]"
patternModel = re.compile(p1)
input_file_Path = 'data/weibo.json'
outfile_Path = 'data/weibo.csv'
InfoList = []
with open(input_file_Path, 'r',encoding='UTF-8') as file:
    content = json.loads(file.read(),strict=False)
    # print(temp)
    for data in content:
        # url = data['info:url']
        try:
            release_Date = timeChange(data['info:created_at'])
        except Exception:
            release_Date = ''
        try:
            title = data['info:title']
        except Exception:
            title = ''
        text = data['info:text']
        forward_Name = data['info:source']
        ID = data['info:userId']
        try:
            attitudes_count = data['info:attitudes_count']
        except Exception:
            attitudes_count = '0'
        if attitudes_count == '':
            attitudes_count = '0'
        try:
            comments_count = data['info: comments_count']
        except Exception:
            comments_count = '0'
        if comments_count == '':
            comments_count = '0'
        '''
        #提取关键词(限定数量)
        KeywordNum = math.floor( len(text) / 150) + 1
        if KeywordNum > 5: KeywordNum = 5
        keywords = analyse.extract_tags(text,topK = KeywordNum)
        source_Name = []
        result = jieba.cut(text, cut_all = False)
        # print(','.join(result))
        for i in result:
            match_result = re.findall(patternModel, i)
            for info in match_result:
                # print(info)
                #去除单个字以及两个字
                if len(info) > 2:
                    # print(info)
                    source_Name.append(info)
        '''
        keywords = ' '
        source_Name = 'null'
        InfoTemp = Info_Struct(ID, release_Date, title, text,forward_Name, source_Name, attitudes_count,
                               comments_count, keywords)
        InfoList.append(InfoTemp)

with open(outfile_Path, 'w', encoding='gb18030') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['ID', 'username', 'release_Date', 'title', 'text',
                            'attitudes_count', 'comments_count', 'url'])
        for info in InfoList:
            if info.release_Date != '':
                csvWriter.writerow([info.ID, info.forward_Name, info.release_Date, info.title, info.text,
                                 info.attitudes_count, info.comments_count, info.keywords])
        csvFile.close()
print("write over")
