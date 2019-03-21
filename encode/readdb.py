# -*- coding: utf-8 -*-

import os
import errno

# import sentencepiece as spm
import re
import logging
import math

# from prepro_hparams import Hparams
from db_operation import DBOperation


if __name__ == '__main__':

    # 从数据库读入整体数据
    db_path = './js_corpus_final_top_1000.db'   # 数据库文件
    op = DBOperation(db_path, 'corpus')
    result = op.query_all()   # result为整体数据,格式为：list[str]
    # print(result)
    i = 0
    for line in result:
        line = line[0].decode('utf-8')   # 注意这里的操作
        print(len(line))
        i = i + 1
        if i > 2000:
            break
