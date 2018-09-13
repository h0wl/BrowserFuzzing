# coding:utf8
import os

from statisticTool import tokenize


def filtrate(threshold, file_type):
    repo_path = '../BrowserFuzzingData/result/' + file_type
    if os.path.isdir(repo_path):  # 判断repo_path是否是一个文件夹
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                with open(repo_path + '/' + file, 'rb') as f:
                    file_content = f.read()
                    if (tokenize(file_content) / 100) > threshold:
                        os.remove(repo_path + '/' + file)

    print ('execute filtration finished.')


if __name__ == '__main__':
    filtrate(9, 'html')
