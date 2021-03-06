# coding: utf-8
from __future__ import print_function

import os
import time

import numpy as np
import tensorflow as tf
import random
from read_utils import get_batch_generator


def pick_top_n(preds, vocab_size, top_n=5):
    p = np.squeeze(preds)
    # 将除了top_n个预测值的位置都置为0
    p[np.argsort(p)[:-top_n]] = 0
    # 归一化概率
    p = p / np.sum(p)
    # 随机选取一个字符
    c = np.random.choice(vocab_size, 1, p=p)[0]
    return c


class CharRNN:
    def __init__(self, num_classes, num_seqs=64, num_steps=50,
                 lstm_size=128, num_layers=2, learning_rate=0.001,
                 grad_clip=5, sampling=False, train_keep_prob=0.5, use_embedding=False, embedding_size=128):
        if sampling is True:
            num_seqs, num_steps = 1, 1
        else:
            num_seqs, num_steps = num_seqs, num_steps

        self.num_classes = num_classes
        self.num_seqs = num_seqs
        self.num_steps = num_steps
        self.lstm_size = lstm_size
        self.num_layers = num_layers
        self.learning_rate = learning_rate
        self.grad_clip = grad_clip
        self.train_keep_prob = train_keep_prob
        self.use_embedding = use_embedding
        self.embedding_size = embedding_size

        tf.reset_default_graph()
        self.build_inputs()
        self.build_lstm()
        self.build_loss()
        self.build_optimizer()
        self.saver = tf.train.Saver(max_to_keep=1000)

    def build_inputs(self):
        with tf.name_scope('inputs'):
            self.inputs = tf.placeholder(tf.int32, shape=(
                self.num_seqs, self.num_steps), name='inputs')
            self.targets = tf.placeholder(tf.int32, shape=(
                self.num_seqs, self.num_steps), name='targets')
            self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

            # 对于中文，需要使用embedding层
            # 英文字母没有必要用embedding层
            if self.use_embedding is False:
                self.lstm_inputs = tf.one_hot(self.inputs, self.num_classes)
            else:
                with tf.device("/cpu:26") and tf.device("/cpu:27") and tf.device("/cpu:28") \
                     and tf.device("/cpu:29") and tf.device("/cpu:30") and tf.device("/cpu:31") \
                     and tf.device("/cpu:32") and tf.device("/cpu:33") and tf.device("/cpu:34") \
                     and tf.device("/cpu:35") and tf.device("/cpu:36") and tf.device("/cpu:37") \
                     and tf.device("/cpu:38") and tf.device("/cpu:39") and tf.device("/cpu:40") \
                     and tf.device("/cpu:41"):
                    embedding = tf.get_variable('embedding', [self.num_classes, self.embedding_size])
                    self.lstm_inputs = tf.nn.embedding_lookup(embedding, self.inputs)

    def build_lstm(self):
        # 创建单个cell并堆叠多层
        def get_a_cell(lstm_size, keep_prob):
            lstm = tf.nn.rnn_cell.LSTMCell(lstm_size)
            drop = tf.nn.rnn_cell.DropoutWrapper(lstm, output_keep_prob=keep_prob)
            return drop

        with tf.name_scope('lstm'):
            cell = tf.nn.rnn_cell.MultiRNNCell(
                [get_a_cell(self.lstm_size, self.keep_prob) for _ in range(self.num_layers)]
            )
            self.initial_state = cell.zero_state(self.num_seqs, tf.float32)

            # 通过dynamic_rnn对cell展开时间维度
            self.lstm_outputs, self.final_state = tf.nn.dynamic_rnn(cell, self.lstm_inputs,
                                                                    initial_state=self.initial_state)

            # 通过lstm_outputs得到概率
            seq_output = tf.concat(self.lstm_outputs, 1)
            x = tf.reshape(seq_output, [-1, self.lstm_size])

            with tf.variable_scope('softmax'):
                softmax_w = tf.Variable(tf.truncated_normal([self.lstm_size, self.num_classes], stddev=0.1))
                softmax_b = tf.Variable(tf.zeros(self.num_classes))

            self.logits = tf.matmul(x, softmax_w) + softmax_b
            self.proba_prediction = tf.nn.softmax(self.logits, name='predictions')

    def build_loss(self):
        with tf.name_scope('loss'):
            y_one_hot = tf.one_hot(self.targets, self.num_classes)
            y_reshaped = tf.reshape(y_one_hot, self.logits.get_shape())
            loss = tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=y_reshaped)
            self.loss = tf.reduce_mean(loss)

    def build_optimizer(self):
        # 使用clipping gradients
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.loss, tvars), self.grad_clip)
        train_op = tf.train.AdamOptimizer(self.learning_rate)
        self.optimizer = train_op.apply_gradients(zip(grads, tvars))

    def train(self, max_steps, save_path, validate_every_n_steps, log_every_n):
        self.session = tf.Session()
        validating_loss = 10000
        with self.session as sess:
            sess.run(tf.global_variables_initializer())
            new_state = sess.run(self.initial_state)
            training_batch_generator = get_batch_generator('training', self.num_seqs, self.num_steps)
            validating_batch_generator = get_batch_generator('validating', self.num_seqs, self.num_steps)
            step = 0
            for x, y in training_batch_generator:
                step += 1
                start = time.time()
                feed = {self.inputs: x,
                        self.targets: y,
                        self.keep_prob: self.train_keep_prob,
                        self.initial_state: new_state}
                batch_loss, new_state, _ = sess.run([self.loss,
                                                     self.final_state,
                                                     self.optimizer],
                                                    feed_dict=feed)

                end = time.time()
                # control the print lines
                if step % log_every_n == 0:
                    print('step: {}/{} '.format(step, max_steps),
                          'loss: {:.4f}... '.format(batch_loss),
                          '{:.4f} sec/batch'.format((end - start)))
                # 每隔validate_every_n_steps验证一下，如果loss比较低，就保存模型
                if step % validate_every_n_steps == 0:
                    temp_validating_loss = self.validate(validating_batch_generator, new_state, sess)

                    if temp_validating_loss < validating_loss:
                        self.saver.save(sess, os.path.join(save_path, 'model'), global_step=step)
                        validating_loss = temp_validating_loss
                if step >= max_steps:
                    break

            # TODO: Change Logic
            self.saver.save(sess, os.path.join(save_path, 'model'), global_step=step)

    def validate(self, batch_generator, state, sess):
        x, y = batch_generator.__next__()
        feed = {self.inputs: x,
                self.targets: y,
                self.keep_prob: self.train_keep_prob,
                self.initial_state: state}
        validating_batch_loss, _, __ = sess.run([self.loss,
                                                 self.final_state,
                                                 self.optimizer],
                                                feed_dict=feed)
        return validating_batch_loss

    def sample(self, n_samples, prime, vocab_size, word_to_int):
        samples = [c for c in prime]
        sess = self.session
        new_state = sess.run(self.initial_state)
        preds = np.ones((vocab_size,))  # for prime=[]
        for c in prime:
            x = np.zeros((1, 1))
            # 输入单个字符
            x[0, 0] = c
            feed = {self.inputs: x,
                    self.keep_prob: 1.,
                    self.initial_state: new_state}
            preds, new_state = sess.run([self.proba_prediction, self.final_state],
                                        feed_dict=feed)

        c = pick_top_n(preds, vocab_size)
        # 添加字符到samples中
        samples.append(c)

        # 随机化代码长度
        random_length = random.randint(200, n_samples)
        # 不断生成字符，直到达到指定数目
        i = 0
        for i in range(random_length):
            x = np.zeros((1, 1))
            x[0, 0] = c
            feed = {self.inputs: x,
                    self.keep_prob: 1.,
                    self.initial_state: new_state}
            preds, new_state = sess.run([self.proba_prediction, self.final_state],
                                        feed_dict=feed)

            c = pick_top_n(preds, vocab_size)
            samples.append(c)

        while c != word_to_int(';') and i < 6000:
            x = np.zeros((1, 1))
            x[0, 0] = c
            feed = {self.inputs: x,
                    self.keep_prob: 1.,
                    self.initial_state: new_state}
            preds, new_state = sess.run([self.proba_prediction, self.final_state],
                                        feed_dict=feed)

            c = pick_top_n(preds, vocab_size)
            samples.append(c)
            i += 1

        offset = samples.count(word_to_int('{')) - samples.count(word_to_int('}'))
        for i in range(0, offset):
            samples.append(word_to_int('}'))

        return np.array(samples)

    def load(self, checkpoint):
        self.session = tf.Session()
        self.saver.restore(self.session, checkpoint)
        print('Restored from: {}'.format(checkpoint))
