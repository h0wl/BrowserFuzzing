# -*- coding: utf-8 -*-
#/usr/bin/python2
'''
Feb. 2019 by kyubyong park.
kbpark.linguist@gmail.com.
https://www.github.com/kyubyong/transformer

Inference
'''

import os

import tensorflow as tf

from data_load import get_batch_gen
from model import Transformer
from hparams import Hparams
from utils import get_hypotheses, calc_bleu, postprocess, load_hparams
import logging

logging.basicConfig(level=logging.INFO)

# # 获取参数，并将其保存到文件中
logging.info("# hparams")
hparams = Hparams()
parser = hparams.parser
hp = parser.parse_args()
load_hparams(hp, hp.ckpt)

logging.info("# Prepare test batches")

# test数据集，   batches次数，     总数据集长度                 注意2个都是 test1
test_batches, num_test_batches, num_test_samples = get_batch_gen(
                                                    100000, 100000,
                                                    hp.vocab, 1,
                                                    shuffle=False)

iter = tf.data.Iterator.from_structure(test_batches.output_types, test_batches.output_shapes)
xs, ys = iter.get_next()   # 在 test中，xs == ys

test_init_op = iter.make_initializer(test_batches)


logging.info("# Load model")
m = Transformer(hp)   # 执行了 Transformer.__init__()初始化方法

# 定义了预测操作： y_hat
y_hat = m.gen_js(xs, ys)   # 这里的 xs和ys都是同一组数据

logging.info("# Session")
with tf.Session() as sess:

    # ckpt为一个最新的 checkpoint路径
    ckpt_ = tf.train.latest_checkpoint(hp.ckpt)
    ckpt = hp.ckpt if ckpt_ is None else ckpt_   # None: ckpt is a file. otherwise dir.
    saver = tf.train.Saver()

    # 恢复模型
    saver.restore(sess, ckpt)

    sess.run(test_init_op)
    # 执行预测步骤:
    logging.info("# get hypotheses")

    hypotheses = []
    h = sess.run(y_hat)
    hypotheses.extend(h.tolist())

    print(hypotheses)
    hypotheses = postprocess(hypotheses, m.idx2token)
    print(hypotheses)



    #
    # # 将结果写入到 testdir中
    # logging.info("# write results")
    # model_output = ckpt.split("/")[-1]
    # if not os.path.exists(hp.testdir): os.makedirs(hp.testdir)
    # translation = os.path.join(hp.testdir, model_output)
    # with open(translation, 'w') as fout:
    #     fout.write("\n".join(hypotheses))


