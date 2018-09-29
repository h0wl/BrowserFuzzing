# coding:utf8

import os


def read_corpus(repository_path):
    if os.path.isdir(repository_path):
        for root, dirs, files in os.walk(repository_path):  # 遍历目录
            for file in files:  # 遍历当前文件
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    file_content = f.read()
                    content_of_corpus.append(file_content)
    else:
        print(repository_path + ' is not an directory !')


content_of_corpus = []
if __name__ == '__main__':
    repository_path = '../BrowserFuzzingData/result/html'
    read_corpus(repository_path)
    print("Read Out " + str(content_of_corpus.__len__()) + " Files From Corpus")
