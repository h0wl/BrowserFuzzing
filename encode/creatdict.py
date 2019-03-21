import os
import errno

# import sentencepiece as spm
import re
import logging
import math

# from prepro_hparams import Hparams
from db_operation import DBOperation

def readdb():
    db_path = './js_corpus_final_top_1000.db'  # 数据库文件
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
    split_list2 = ['+', '-', '=', '<', '>']
    doublesplit = ['++','+=','--','-=','*=','%=','<=','<<','<<=','>=','>>','>>=','>>>=','!=','!==','==','===','\'','\"','\\','\t','\&','\n','\r','\b','\f']
    ESC = ['\'','"','\\','t','&','n','r','b','f']
    word = ''
    oprater = ''
    for i in range(len(code)):

        if code[i] not in split_list:
            word += code[i]
        else:
            if word != '':
                tokens.append(word)
                word = ''
            #         处理操作符


            if code[i] != ' ':
                oprater += code[i]
                if i+1 < len(code):
                    if code[i] == '\\':
                        if code[i+1] in ESC:
                            continue
                    elif code[i + 1] in split_list2:
                        continue
                    else:
                        # print(oprater)
                        if oprater in doublesplit:
                            if oprater =='\n':
                                oprater = '\\n'
                            if oprater == '\t':
                                oprater == '\\t'
                            tokens.append(oprater)
                            oprater = ''
                        else:
                            for s in range(len(oprater)):
                                tokens.append(oprater[s])
                            oprater = ''

                        # tokens.append(oprater)
                        # oprater = ''

                else:
                    # print(oprater)
                    if oprater in doublesplit:
                        tokens.append(oprater)
                        oprater = ''
                    else:
                        for s in range(len(oprater)):
                            tokens.append(oprater[s])
                        oprater = ''

                    # tokens.append(oprater)
                    # oprater = ''


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

    for line in dbfile:
        line = line[0].decode("UTF-8")

        tokens = code2tokens(line)
        tokenfile.append(tokens)

        count_dict = tokencount(tokens,count_dict)


    # 按照词频从高到低排列
    count_list = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    # 保存字典
    outfile = "./output/jsdict.txt"
    dictwithoutlast5 = "./output/dictwithoutlast5.txt"
    with open(outfile, 'w', encoding="UTF-8")as outputfile:
        for token in count_list:
            # print(token[0] + "\t" + str(token[1]))

            outputfile.write(token[0] + "\t" + str(token[1]))
            outputfile.write('\n')

    num = range(len(count_list))
    tokenonly = []
    for token in count_list:
        if token[1] > 5:
            tokenonly.append(token[0])
    tokendict = list(zip(tokenonly,range(len(count_list))))
    with open(dictwithoutlast5, 'w', encoding="UTF-8")as outputdict:

        for token in tokendict:
            # print(token[1])

                # print()
            # print(token[0] + "\t" + str(token[1]))
            outputdict.write(token[0] + "\t" + str(token[1]))
            outputdict.write('\n')

    return tokendict,tokenfile



