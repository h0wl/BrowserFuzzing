# -*- coding: utf-8 -*-
"""
"""
import numpy as np
from numpy import linalg as la
import math


def unifine(x,maxlen):
    vector = list(x)
    for i in range(maxlen - len(x)):
        vector.append(0)
    return vector


def bit_product_sum(x, y):
    return sum([item[0] * item[1] for item in zip(x, y)])

#余弦
def cosine_similarity(x, y, norm=False):
    """ 计算两个向量x和y的余弦相似度 """


    #两两统一向量维度
    if len(x) != len(y):
        maxlen = 3000
        if max(len(x),len(x)) < maxlen:
            x = unifine(x,max(len(x),len(y)))
            y = unifine(y,max(len(x),len(y)))
        else:
            if len(x) > maxlen:
                x = x[:maxlen]
            if len(y) > maxlen:
                y = y[:maxlen]
            x = unifine(x, maxlen)
            y = unifine(y, maxlen)



    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)

    # method 1
    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))
    if math.isnan(cos):
        cos = 0

    # method 2
    # cos = bit_product_sum(x, y) / (np.sqrt(bit_product_sum(x, x)) * np.sqrt(bit_product_sum(y, y)))

    # method 3
    # dot_product, square_sum_x, square_sum_y = 0, 0, 0
    # for i in range(len(x)):
    #     dot_product += x[i] * y[i]
    #     square_sum_x += x[i] * x[i]
    #     square_sum_y += y[i] * y[i]
    # cos = dot_product / (np.sqrt(square_sum_x) * np.sqrt(square_sum_y))

    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内
#欧式
def ecludSim(inA, inB):
    return 1.0 / (1.0 + la.norm(inA - inB))  # inA，inB是列向量


# def pearSim(inA, inB):
#     if len(inA) < 3:
#         return 1.0
#     else:
#
#         #         print("corrcoef(inA,inB,rowvar=0)",corrcoef(inA,inB,rowvar=0))
#         # 对称矩阵，且corrcoef是x1x1，x1x2,x2x1,x2x2这四者系数。
#         #         print("corrcoef(inA,inB,rowvar=0)[0]",corrcoef(inA,inB,rowvar=0)[0])
#         # 由于两个变量，所以取第一行就是x1对所有变量的线性相关性，协方差。
#         #         print("corrcoef(inA,inB,rowvar=0)[0][1]",corrcoef(inA,inB,rowvar=0)[0][1])
#         # 第一行第二列就是x2x1，第二列和第二行一样都是第二个变量对所有其他变量的线性相关性。
#         return 0.5 + 0.5 * corrcoef(inA, inB, rowvar=0)[0][1]



