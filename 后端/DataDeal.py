# -*- coding:utf-8 -*-
import re

openFilename = "微信.txt"
writeFilename = "weixin.json"
skip = 2

file_text = open(openFilename, encoding='UTF-8').read()
file_write = open(writeFilename, 'w', encoding='UTF-8')
test_list = file_text.split('},')
if file_text.strip()[-1] == '}':
    skip = 1
result_list = []
total = len(test_list)
not_match_count = 0
#所有属性的集合set容器
DataContent = set()
#添加属性到容器中
for i in range(len(test_list)):
    item = test_list[i]
    searchRes = re.findall('\'info:([\s\S]*?)\'', item)
    for j in searchRes:
        DataContent.add(j)
for i in DataContent:
    print(i)
for i in range(len(test_list)):
    item = test_list[i]
    matchFlag = False
    #先是左花括号
    content = '{\n'
    for data in DataContent:
        pattern = '\'info:( )?' + data + '\':( )?\'[\s\S]*?\''
        #进行模式匹配
        searchRes = re.search(pattern, item)
        if searchRes:
            result = re.sub('\n', " ", item[searchRes.start():searchRes.end()])
            content += result
            #添加逗号
            content += ',\n'
            matchFlag = True
    if matchFlag:
        #去除最后一个逗号，然后添加 }, 或者 }
        content = content[:-2]
        # 因为最后会有一个空的匹配结果，所以要在len(test_list) - skip时候将 }, 换为 } 代表文件的结束
        if i != (len(test_list) - skip):
            content += '\n},\n'
        else:
            content += '\n}\n'
        # print(temp)
        result_list.append(content)
    else:
        print(item)
        print("a text not match")
        not_match_count += 1

print('未匹配的数目占总数的',not_match_count/total)
result_test = "".join(result_list)
#先将文中出现的所有英文双引号转换问中文双引号，再将所有单引号转换为英文双引号
result_test = result_test.replace('\"','“')
result_test = result_test.replace('\'','\"')
#编码问题，将\xXXX的部分然后处理&
result_test = result_test.replace('\\','&')
# print(result_test)
file_write.write('[\n')
file_write.write(result_test)
file_write.write(']\n')
print("write over")