# coding:utf8
import os


def count_tokens(file_type):
    counter = {}
    repo_path = '../BrowserFuzzingData/result/' + file_type
    if os.path.isdir(repo_path):  # 判断repo_path是否是一个文件夹
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                with open(repo_path + '/' + file, 'rb') as f:
                    file_content = f.read()
                    count = tokenize(file_content) / 100
                    if count in counter:
                        counter.__setitem__(count, counter.get(count) + 1)
                    else:
                        counter.__setitem__(count, 1)
    return counter


def tokenize(file_content):
    word = ''
    counter = 0
    for char in file_content:
        if str(char).isdigit() | str(char).isalpha() | (str(char) == '_'):
            word += str(char)
        else:
            if word.__len__() != 0:
                counter += 1
                word = ''
    if word.__len__() != 0:
        counter += 1
    return counter


if __name__ == '__main__':
    counter = count_tokens('html')
    for key, value in counter.items():
        print(str(key) + ' : ' + str(value))
