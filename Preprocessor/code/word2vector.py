# coding:utf8
# 引入 word2vec
# 引入日志配置
import os

from gensim.models import word2vec


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()


def tokenize(file_content, model):
    word = ''
    for char in file_content:
        if not ((str(char) == ' ') | (str(char) == '\n') | (str(char) == '\r') | (str(char) == '=')):
            word += str(char)
        else:
            if word.__len__() != 0:
                print (model[word])
                word = ''
    if word.__len__() != 0:
        print (model[word])


# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# sentences = MySentences('../BrowserFuzzingData/result/html')
# model = gensim.models.Word2Vec(sentences)
# model.save('../BrowserFuzzingData/result/html.model')
file_path = '../BrowserFuzzingData/result/html/nav.html'
model = word2vec.Word2Vec.load('../BrowserFuzzingData/result/html.model')
with open(file_path, 'rb') as f:
    file_content = f.read()
tokenize(file_content, model)
