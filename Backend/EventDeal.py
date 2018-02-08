# 划分时间窗口

import pandas as pd
import numpy as np
import re
import math
from datetime import datetime
from numpy.core.defchararray import isdigit
from gensim import corpora, models, similarities
from collections import defaultdict
import jieba
from jieba import analyse
import json

# global var
stopwords = []
nameDictionary= []


def creatStopWords(filename):
    stopfile = open(filename, encoding='UTF-8')
    for line in stopfile:
        stopwords.append(line.strip())

def creatNameDictionary(filename):
    namefile = open(filename, encoding='UTF-8')
    for line in namefile:
        nameDictionary.append(line.strip())

class Info:
    def __init__(self, id, username, date, title, text, attitudecount=0, commentcount=0, url=' '):
        self.id = id
        if str(username) == 'nan':
            self.username = ''
        else:
            self.username = username
        self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        if str(title) == 'nan':
            self.title = ''
        else:
            self.title = title
        if str(text) == 'nan':
            self.text = ''
        else:
            self.text = text
        self.attitudecount = attitudecount
        self.commentcount = commentcount
        self.url = url


class TimeWindow:
    def __init__(self, kind, date, type):
        """
        :param kind:int kind = 0: dayCountList   kind = 1: hourCountList   kind = 2 : tenMinutesCountList
        :param date: datetime
        :param type: type = 0 official data   type = 1 unofficial data
        """
        self.kind = kind
        self.window_date = date
        self.count = 0
        self.datatype = type
        self.infolist = []
        self.word_graph = []
        self.word_dict = {}             # <word, num>
        self.word_list = []
        self.event_list = []

    def addInfo(self, info_data):
        self.count += 1
        self.infolist.append(info_data)

    def creatWordDict(self):
        """
        creat self.word_dict && self.word_list according to self.infolist, select top 10% of the keywords
        :return: Null
        """
        temp_dict = {}
        word_num = 0
        for info_item in self.infolist:
            #　print(info_item.title)
            # print(info_item.text)

            # info_weight 待调
            info_weight = info_item.attitudecount + 2 * info_item.commentcount
            # print(info_weight)
            keynum = math.ceil(len(info_item.title) / 5)
            keywords = analyse.extract_tags(info_item.title, topK=keynum)
            for word_item in keywords:
                if word_item in temp_dict:
                    temp_dict[word_item] += 5
                else:
                    temp_dict[word_item] = info_weight + 5

            text_list = re.split('，|。|？|！', info_item.text)
            for sentence in text_list:
                # print(sentence)
                keynum = math.ceil(len(sentence) / 10)
                keywords = analyse.extract_tags(sentence, topK=keynum)
                # print(keywords)
                for word_item in keywords:
                    if word_item in temp_dict:
                        temp_dict[word_item] += 1
                    else:
                        temp_dict[word_item] = 1

        word_temp_list = sorted(temp_dict.items(), key=lambda item: item[1], reverse=True)  # 出来后是列表形式
        topnum = math.ceil(len(word_temp_list) / 10)

        # creat self.word_dict
        i = 0
        while word_num < topnum:
            w = word_temp_list[i][0]
            if not isdigit(w) and w not in stopwords:
                self.word_dict[w] = word_num
                self.word_list.append(w)
                word_num += 1
                # print(word_temp_list[i])
            i += 1

    def creatWordGraph(self):
        """
        creat self.word_graph  according to self.infolist and self.word_dict
        """
        graph_num = len(self.word_dict)
        self.word_graph = np.zeros((graph_num, graph_num))
        for info_item in self.infolist:
            # print(info_item.title)
            #　print(info_item.text)
            temp_title_list = []
            # info_weight 待调
            info_weight = info_item.attitudecount + 2 * info_item.commentcount
            # dataprint(info_weight)
            keynum = math.ceil(len(info_item.title) / 5)
            keywords = analyse.extract_tags(info_item.title, topK=keynum)
            for word_item in keywords:
                if word_item in self.word_dict:
                    temp_title_list.append(self.word_dict[word_item])

            if len(temp_title_list) > 1:
                self.updateWordGraph(temp_title_list, 5 + info_weight)

            text_list = re.split('，|。|？|！', info_item.text)

            for sentence in text_list:

                temp_sentence_list = []
                keynum = math.ceil(len(sentence) / 10)
                keywords = analyse.extract_tags(sentence, topK=keynum)
                for word_item in keywords:
                    if word_item in self.word_dict:
                        temp_sentence_list.append(self.word_dict[word_item])
                if len(temp_sentence_list) > 1:
                    self.updateWordGraph(temp_sentence_list, 1)

            '''
            temp_text_list = []
            for sentence in text_list:
                keynum = math.ceil(len(item) / 10)
                keywords = analyse.extract_tags(sentence, topK=keynum)
                for word_item in keywords:
                    if word_item in self.word_dict and word_item not in temp_text_list:
                        temp_text_list.append(self.word_dict[word_item])
            if len(temp_text_list) > 1:
                self.updateWordGraph(temp_text_list, 1)
            '''

    def updateWordGraph(self, data_list, weight):
        """
        update the weight value of self.word_graph according to the data_list
        used by self.creatWordGraph
        :param data_print(data_list)list: the list of word_num(int)
        :param weight:  the weight should be added
        """
        print(data_list, weight)
        for i in range(len(data_list)):
            word_i_num = data_list[i]
            for j in range(i+1, len(data_list)):
                word_j_num = data_list[j]
                self.word_graph[word_i_num][word_j_num] += weight
                self.word_graph[word_j_num][word_i_num] += weight

    def creatEventList(self):
        """
        extract event from word_graph
        :return: null
        """
        temp_word_list = []
        threshold = 0

        for item in self.word_list:
            temp_word_list.append(item)

        # 去除图中孤立点
        for i in range(len(self.word_graph)):
            isolated_point = 1
            for j in range(len(self.word_graph)):
                if self.word_graph[i][j] > threshold:
                    isolated_point = 0          # 存在连接, 则不是孤立点
                    break
            if isolated_point == 1:     # 孤立点
                temp_word_list.pop(i)



    def writeIntoFile(self, outFilePath, similarContentDic):
        # 关联的数组的个数
        LinkedArraySize = len(similarContentDic)
        AllArrayDic = {}
        if self.kind == 0:
            kind_str = "one day"
        elif self.kind == 1:
            kind_str = "one hour"
        else:
            kind_str = "ten minutes"
        # 文件中的节点相连数组总个数
        AllArrayDic['LinkedArraySize'] = LinkedArraySize
        AllArrayDic['Date'] = self.window_date.strftime("%Y-%m-%d %H:%M:%S")
        AllArrayDic['TimeWindowLen'] = kind_str
        count_array = 1
        for i in similarContentDic:
            nodeSize = len(similarContentDic[i])
            AllNodeDic = {}
            keywords_list = []
            keywords_dict = {}
            # 一个数组的节点个数
            AllNodeDic['nodeSize'] = nodeSize
            count_node = 1
            # 得到所有节点名字的数组
            AllNodeNameArray = [str(data.username) for data in similarContentDic[i]]
            AllNodeDic['AllNodeNameArray'] = AllNodeNameArray
            for data in similarContentDic[i]:
                nodeAttr = 'node_' + str(count_node)
                ID = data.id
                nodeName = str(data.username)
                # print(nodeName)

                # 去掉自身名字
                # linkedNodeNameArray = AllNodeNameArray.copy()
                # linkedNodeNameArray.remove(nodeName)
                nodeInfo = {}
                nodeDic = {}
                nodeDic['ID'] = ID
                nodeDic['nodeName'] = nodeName
                # nodeDic['linkedNodeNameArray'] = linkedNodeNameArray
                nodeDic['nodeInfo'] = nodeInfo

                # 将节点信息添加到字典中
                AllNodeDic[nodeAttr] = nodeDic
                count_node += 1

                # 提取题目关键词并将其加入keywords_dict字典中
                keynum = math.ceil(len(data.title) / 5)
                keywords = analyse.extract_tags(data.title, topK=keynum)
                # print(keynum)
                # print(keywords)
                for word_item in keywords:
                    if word_item in keywords_dict:
                        keywords_dict[word_item] += 2
                    else:
                        keywords_dict[word_item] = 2

                # 提取text关键词并将其加入keywords_dict字典中
                keynum = math.ceil(len(data.text) / 30)
                keywords = analyse.extract_tags(data.text, topK=keynum)
                # print(keynum)
                # print(keywords)
                for word_item in keywords:
                    if word_item in keywords_dict:
                        keywords_dict[word_item] += 1
                    else:
                        keywords_dict[word_item] = 1


            LinkedarrayAttr = 'LinkedArray_' + str(count_array)
            # 一个相连数组信息添加到字典
            AllArrayDic[LinkedarrayAttr] = AllNodeDic
            count_array += 1

            # 处理关键词字典
            keywords_temp_list = sorted(keywords_dict.items(), key=lambda item: item[1], reverse=True)  # 出来后是列表形式
            if len(keywords_temp_list) > 20:
                topnum = 10
            else:
                topnum = math.ceil(len(keywords_temp_list) / 2)

            # creat self.word_dict
            i = 0
            word_num = 0
            while word_num < topnum and i < len(keywords_temp_list):
                w = keywords_temp_list[i][0]
                if not isdigit(w) and w not in stopwords:
                    keywords_list.append(w)
                    word_num += 1
                    # print(keywords_temp_list[i])
                i += 1
            AllNodeDic['keywords'] = keywords_list


        # 写入文件
        with open(outFilePath, 'w', encoding='utf-8') as file_object:
            json.dump(AllArrayDic, file_object, ensure_ascii=False, indent=4)
            file_object.close()

    def calculateSimilarity(self, SplitEffect):
        compareRate = 0.2
        DataCollection = self.infolist.copy()
        dateStr = self.window_date.strftime("%Y-%m-%d-%H-%M")
        #总的文本个数
        SplitEffect[dateStr].append(len(DataCollection))
        count = 0
        similarContentDic = defaultdict(list)
        texts = []
        #每个data为一个Info结构体
        for data in DataCollection:

            # print(data)
            count += 1
            # print(data.text)
            # print(count)
            # print(data['release_Date'])

            # 要比较的文本
            text = data.text
            KeywordNum = math.floor(len(text) / 30) + 1
            new_text = analyse.extract_tags(text, topK=KeywordNum)
            # print(new_text)
            # 若小于2，直接添加
            if len(texts) <= 5:
                texts.append(new_text)
                # 添加数据进字典
                similarContentDic[len(texts)].append(data)
                continue

            # 创建字典（单词与编号之间的映射）
            dictionary = corpora.Dictionary(texts)
            # print(dictionary.token2id)

            # 将要比较的文档转换为向量（词袋表示方法）
            new_vec = dictionary.doc2bow(new_text)
            # 建立语料库
            # 将每一篇文档转换为向量
            corpus = [dictionary.doc2bow(text) for text in texts]
            # print(corpus)

            # 初始化模型
            # 初始化一个tfidf模型,可以用它来转换向量（词袋整数计数）表示方法为新的表示方法（Tfidf 实数权重）
            tfidf = models.TfidfModel(corpus)
            # 将整个语料库转为tfidf表示方法
            corpus_tfidf = tfidf[corpus]
            # for doc in corpus_tfidf:
            #     print(doc)
            # 创建索引
            index = similarities.MatrixSimilarity(corpus_tfidf)

            # 相似度计算
            new_vec_tfidf = tfidf[new_vec]  # 将要比较文档转换为tfidf表示方法

            # 计算要比较的文档与语料库中每篇文档的相似度
            sims = index[new_vec_tfidf]
            rate = max(sims)
            index = sims.tolist().index(rate)
            if rate >= compareRate:
                similarContentDic[index + 1].append(data)
                # print('here!!!!!!!!!!!!!!!!!!!!!!!')
                # print(sims)
            else:
                # print(rate)
                texts.append(new_text)
                similarContentDic[len(texts)].append(data)
                # print(sims)

        SplitEffect[dateStr].append(len(similarContentDic))
        # 划分结果此时存储到similarContentDic中，键为分割的序号，值为为同一类别的数据
        # 将结果写入文件
        if self.datatype == 0:   # official data
            out_file_path = "result/official/" + dateStr + '.json'
        else : # official data
            out_file_path = "result/unofficial/" + dateStr + '.json'

        self.writeIntoFile(out_file_path, similarContentDic)
        similarContentDic.clear()
        texts.clear()

    def findForward(self):
        DataCollection = self.infolist.copy()
        dateStr = self.window_date.strftime("%Y-%m-%d-%H-%M")
        # 匹配模式/xx网、xx社、xx报
        pattern = ".*?[网社报]"
        patternModel = re.compile(pattern)
        relationDic = defaultdict(list)
        tempList = []
        count = 0
        # 每个data为一个Info结构体
        for data in DataCollection:
            count += 1
            # print(count)
            # 获取文本内容
            text_Content = data.text
            nodeName = data.username
            # 进行分词处理
            result = jieba.cut(text_Content, cut_all=False)
            for i in result:
                match_result = re.findall(patternModel, i)
                for info in match_result:
                    if info in nameDictionary and info not in relationDic[nodeName]:
                        # print(info)
                        relationDic[nodeName].append(info)
        # 转发关系已经添加到relationDic中
        outFilePath = 'result/official_forward/' + dateStr + '.json'
        self.writeForwardIntoFile(outFilePath, relationDic)

    def writeForwardIntoFile(self, outFilePath, relationDic):
        # 关联的数组的个数
        nodeSize = len(relationDic)
        AllNodeDic = {}
        # 文件中的节点相连数组总个数
        if self.kind == 0:
            kind_str = "one day"
        elif self.kind == 1:
            kind_str = "one hour"
        else:
            kind_str = "ten minutes"
        AllNodeDic['nodeSize'] = nodeSize
        AllNodeDic['date'] = self.window_date.strftime("%Y-%m-%d %H:%M:%S")
        AllNodeDic['timeWindowLen'] = kind_str
        count_node = 1
        # i 为名字
        for i in relationDic:
            infoDic = {}
            infoDic['name'] = i
            infoDic['forwardNameArray'] = relationDic[i]
            AllNodeDic['node_' + str(count_node)] = infoDic
            count_node += 1

        # 写入文件
        with open(outFilePath, 'w', encoding='utf-8') as file_object:
            json.dump(AllNodeDic, file_object, ensure_ascii=False, indent=4)
            file_object.close()


class CountDeal:
    def __init__(self, type, day_hour_para=1000, hourmin_para=1000):
        self.datatype = type    # type = 0, official data,  type = 1, unofficial data
        self.dayhour_para = day_hour_para
        self.hourmin_para = hourmin_para
        self.day_window_list = []
        self.hour_window_list = []
        self.tenmin_window_list = []

    def creatList(self, data):
        self.creatDayList(data)
        self.creatHourList()
        self.creatMinList()

    def creatDayList(self, data):
        """
        creat self.day_window_list according to the data
        :param data: list<Info>  src data with the format of Info
        :return:null
        """
        day_dict = {}  # <date, TimeWindow>
        for item in data:
            year = item.date.year
            month = item.date.month
            day = item.date.day
            temp = datetime(year, month, day)
            if temp in day_dict:
                day_dict[temp].addInfo(item)
            else:
                newwin = TimeWindow(kind=0, date=temp, type=self.datatype)
                newwin.addInfo(item)
                day_dict[temp] = newwin

        day_temp_list = sorted(day_dict.items(), key=lambda item: item[0], reverse=False)  # 出来后是列表形式
        for item in day_temp_list:
            self.day_window_list.append(item[1])

    def creatHourList(self):
        """
        creat self.hour_window_list according to the self.day_window_list
        :return:null
        """
        for win_item in self.day_window_list[:]:
            hour_dict = {}  # <date, TimeWindow>
            if win_item.count >= self.dayhour_para:
                data_temp_list = win_item.infolist
                for item in data_temp_list:
                    year = item.date.year
                    month = item.date.month
                    day = item.date.day
                    hour = item.date.hour
                    temp = datetime(year, month, day, hour)
                    if temp in hour_dict:
                        hour_dict[temp].addInfo(item)
                    else:
                        newwin = TimeWindow(kind=1, date=temp, type=self.datatype)
                        newwin.addInfo(item)
                        hour_dict[temp] = newwin
                hour_temp_list = sorted(hour_dict.items(), key=lambda item: item[0], reverse=False)  # 出来后是列表形式
                for item in hour_temp_list:
                    self.hour_window_list.append(item[1])

                # 删除已经进行拆分的时间窗口
                self.day_window_list.remove(win_item)

    def creatMinList(self):
        """
        creat self.tenmin_window_list according to the self.hour_window_list
        :return:
        """

        for win_item in self.hour_window_list[:]:
            min_dict = {}  # <date, TimeWindow>
            if win_item.count >= self.hourmin_para:
                data_temp_list = win_item.infolist
                for item in data_temp_list:
                    year = item.date.year
                    month = item.date.month
                    day = item.date.day
                    hour = item.date.hour
                    minute = int(item.date.minute / 10) * 10
                    temp = datetime(year, month, day, hour, minute)
                    if temp in min_dict:
                        min_dict[temp].addInfo(item)
                    else:
                        newwin = TimeWindow(kind=2, date=temp, type=self.datatype)
                        newwin.addInfo(item)
                        min_dict[temp] = newwin
                min_temp_list = sorted(min_dict.items(), key=lambda item: item[0], reverse=False)  # 出来后是列表形式
                for item in min_temp_list:
                    self.tenmin_window_list.append(item[1])

                # 删除已经进行拆分的时间窗口
                self.hour_window_list.remove(win_item)

    def dealDayHourMinList(self):
        if self.datatype == 0:   # official data
            path = "logdata/official/"
            # deal official forward
            self.dealTimeWindowForward(self.day_window_list)
            self.dealTimeWindowForward(self.hour_window_list)
            self.dealTimeWindowForward(self.tenmin_window_list)
        else:
            path = "logdata/unofficial/"

        day_log_file = open(path + "daylog.txt",'w')
        day_log_file.write("This is day log file\n\n")
        day_log_file.write("The count of daywindow is:%d \n"% len(self.day_window_list))
        self.dealTimeWindowList(self.day_window_list, day_log_file)
        day_log_file.close()

        hour_log_file = open(path + "hourlog.txt",'w')
        hour_log_file.write("This is hour log file\n\n")
        hour_log_file.write("The count of hourWindow is: %d \n"% len(self.hour_window_list))
        self.dealTimeWindowList(self.hour_window_list, hour_log_file)
        hour_log_file.close()


        min_log_file = open(path + "minlog.txt",'w')
        min_log_file.write("This is min log file\n\n")
        min_log_file.write("The count of hourWindow is: %d \n"% len(self.tenmin_window_list))
        self.dealTimeWindowList(self.tenmin_window_list, min_log_file)
        min_log_file.close()

    def dealTimeWindowList(self, data_list, logFile):
        split_effect = defaultdict(list)
        for item in data_list:
            item.calculateSimilarity(split_effect)

        for i in split_effect:
            logFile.write("\n" + i + "\n")
            logFile.write('划分前类别个数: %d\n' % split_effect[i][0])
            logFile.write('划分后类别个数: %d\n' % split_effect[i][1])

    def dealTimeWindowForward(self, data_list):
        """
        deal official data forward
        :param data_list:
        :return:
        """
        for item in data_list:
            item.findForward()


    def printWindow(self, wintype):
        """
        print window info
        :param type: 0--day  1--hour  2--minute
        :return: null
        """
        if wintype == 0:
            for dayitem in self.day_window_list:
                print(" ", dayitem.kind, dayitem.window_date.strftime('%Y-%m-%d'), dayitem.count)
        elif wintype == 1:
            for houritem in self.hour_window_list:
                print(" ", houritem.kind, houritem.window_date.strftime('%Y-%m-%d %H:%M:%S'), houritem.count)
        elif wintype == 2:
            for minitem in self.tenmin_window_list:
                print(" ", minitem.kind, minitem.window_date.strftime('%Y-%m-%d %H:%M:%S'), minitem.count)
        else:
            print("error: CountDeal printWindow's type out of range %d" % type)


if __name__ == "__main__":
    filename = input("please input the file name(the encoding should be gb18030):")
    type = int(input("please input the data type(official data is 0, unofficial is 1):"))
    stopwords_file_name = "srcdata/stopwords.txt"
    nameDictionary_file_name = "srcdata/NameDictionary.txt"

    data = pd.read_csv(filename, encoding='gb18030')
    data = np.array(data)
    data = np.nan_to_num(data)
    dataList = []
    data = data.tolist()
    for item in data:
        dataList.append(Info(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

    # set global var--stopwords
    creatStopWords(stopwords_file_name)
    creatNameDictionary(nameDictionary_file_name)

    if type == 0:   # official data
        count_deal = CountDeal(type=0, day_hour_para=100, hourmin_para=100)
    elif type == 1:     # unofficial data
        count_deal = CountDeal(type=1, day_hour_para=1000, hourmin_para=1000)
    else:
        count_deal = " "
        print("type error:", type)
        exit(1)

    count_deal.creatList(dataList)
    print("day window:")
    count_deal.printWindow(0)
    print("hour window:")
    count_deal.printWindow(1)
    print("minute window:")
    count_deal.printWindow(2)

    # ount_deal.dealDayHourMinList()
