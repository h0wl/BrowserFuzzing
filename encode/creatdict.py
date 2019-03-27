import os
import errno

# import sentencepiece as spm
import re
import logging
import math

# from prepro_hparams import Hparams
from db_operation import DBOperation



def readdb():
    db_path = '../../BrowserFuzzingData/js_corpus_final_top_1000.db'  # 数据库文件
    op = DBOperation(db_path, 'corpus')
    result = op.query_all()  # result为整体数据,格式为：list[str]
    # print(result)
    return result



# 分解code，还需修改
def code2tokens(code):
    code.replace('\n\n', '\n')
    tokens = []

    split_list = ['.', '\'', '"', ' ', '?', '*', '[', ']', '(', ')', '{', '}', ':', '=', ',', '+', '-', '>', '<', ';',
                  '%','/','!','|','^']
    #检测多个字符的运算符

    doublesplit = ['++','+=','--','-=','*=','%=','<=','<<','<<=','>=','>>','>>=','>>>=','!=','!==','==','===','=>','||','&&','\'','\"','\\','\t','\&','\n','\r','\b','\f']
    split_list2 = ['+', '-', '=', '<', '>', '|', "&",]

    ESC = ['\'','"','\\','\t','\&','\n','\r','\b','\f']
    word = ''
    operator = ''
    #flag为1，表示多位operater，flag为0表示word或者一位operator
    flag = 0

    for i in range(len(code)):

        #一位操作符
        if code[i] in split_list:

            if word != '':
                tokens.append(word)
                word = ''

            if code[i] !=' ':
                operator += code[i]
                flag = 0
                if i+1 < len(code):
                    if i in split_list2:
                        flag = 1
                        continue
        #多位操作符或word
        else:
            #多位操作符
            if flag == 1:
                operator += code[i]
                flag = 0
                if i+1 < len(code):
                    if i in split_list2:
                        flag = 1
                        continue
            #word
            else:
                word += code[i]
                if operator != '':
                    if operator in split_list2:
                        # if operator == '\n':
                        #     operator = '\\n'
                        # if operator == '\t':
                        #     operator = '\\t'
                        tokens.append(operator)
                        operator = ''
                    else:
                        for a in operator:
                            tokens.append(a)
                        operator = ''


    return tokens


def tokencount(tokens, count_dict):
    # 如果字典里有该单词则加1，否则添加入字典
    for str in tokens:
        if str in count_dict.keys():
            count_dict[str] = count_dict[str] + 1
        else:
            count_dict[str] = 1

    return count_dict


def ListFilesToTxt():
    #    文件存放路径
    dir = "G:\\毕设\\浏览器测试\\jstest"
    #    文本输出路径
    outfile = "./output/jsfile.txt"
    files = os.listdir(dir)
    for name in files:
        if name.endswith(".js"):
            #             以追加的的形式打开txt   a表示追加
            with open(outfile, 'a') as f:
                #                  print(name)
                f.write(name)
                f.write('\n')


def creatdict():
    # 获取文件列表
    # ListFilesToTxt()
    # 词频字典
    count_dict = {}
    tokenfile = []

       # # 打开文件（本地列表读取）
    # with open("./output/jsfile.txt", "r") as pathfile:
    # # with open("C:\\Users\\Administrator\\Desktop\\jsfile.txt", "r") as pathfile:
    #     for line in pathfile.readlines():
    #         line = line[:-1]
    #         with open("G:\\毕设\\浏览器测试\\jstest\\" + line, "r", encoding='UTF-8') as codefile:
    #             codes = codefile.read()
    #
    #             tokens = code2tokens(codes)
    #             tokenfile.append(tokens)
    #
    #             count_dict = tokencount(tokens, count_dict)

    dbfile = readdb()
    i = 0
    print("devide")

    for line in dbfile:
        line = line[0].decode("UTF-8")

        tokens = code2tokens(line)

        # print(str(tokens))

        tokenfile.append(tokens)

        count_dict = tokencount(tokens,count_dict)
        i  = i + 1
        if i > 50000:
            break

    count_list = {}

    # 按照词频从高到低排列
    # count_list = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    for token in sorted(count_dict.items(), key=lambda x: x[1], reverse=True):
        count_list.setdefault(token[0],token[1])

    # 保存字典
    outfile = "./output/jsdict.txt"
    dictwithoutlast5 = "./output/dictwithoutlast5.txt"

    with open(outfile, 'w', encoding="UTF-8")as outputfile:
        for key,value in count_list.items():
            # print(token[0] + "\t" + str(token[1]))

            outputfile.write(key + "\t" + str(value))
            outputfile.write('\n')

    num = 0
    # tokenonly = []
    for key,value in count_list.items():
        if value > 5:
            # tokenonly.append(token[0])
            num = num + 1
    # tokendict = list(zip(tokenonly,range(len(count_list))))
    tokendict = {}

    for (x , y) in zip(count_list.keys(),range(num)):
        tokendict.setdefault(x,y)

    with open(dictwithoutlast5, 'w', encoding="UTF-8")as outputdict:

        for key,value in tokendict.items():
            # print(token[1])

                # print()
            # print(token[0] + "\t" + str(token[1]))
            outputdict.write(key + "\t" + str(value))
            outputdict.write('\n')

    return tokendict,tokenfile



