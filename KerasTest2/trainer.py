# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 21:10:42 2018
@author: x00428488
"""
import os

from keras.callbacks import ModelCheckpoint
from keras.layers.core import Dense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential

from generator import TextConverter, batch_generator_one_word
import tensorflow as tf

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
gpuConfig = tf.ConfigProto(allow_soft_placement=True)

# 运行时需要多少再给多少
gpuConfig.gpu_options.allow_growth = True

# 把你的配置部署到session
with tf.Session(config=gpuConfig) as sess:
    pass

convert_text = TextConverter(filename='wonderland.txt')

train_arr = convert_text.text_to_arr(filename='train.txt')
valid_arr = convert_text.text_to_arr(filename='valid.txt')
vocab_size = convert_text.vocab_size
num_seqs = 128
num_steps = 32
train_gene = batch_generator_one_word(train_arr, num_seqs, num_steps, vocab_size)
valid_gene = batch_generator_one_word(valid_arr, num_seqs, num_steps, vocab_size)

# 序贯模型
model = Sequential()
# 嵌入层，实际相当于每个词从索引替换为词向量，input_dim是最大的词索引+1，
# input_length是每个序列里面包含的词汇量，
# out_shape是n_bathes x input_length x output_dim

model.add(Embedding(output_dim=100,
                    input_dim=vocab_size,
                    input_length=num_steps))
# model.add(Dropout(0.35))
# units 是输出空间的维度
model.add(LSTM(units=128, dropout=0.2, return_sequences=True))
model.add(LSTM(units=128, dropout=0.2))
model.add(Dense(units=vocab_size, activation='softmax'))

model.summary()
# 训练模型
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['categorical_accuracy'])

checkpointer = ModelCheckpoint(
    filepath='model-{epoch:02d}.hdf5', verbose=1)
num_epochs = 30

model.fit_generator(train_gene,
                    20000, num_epochs,
                    validation_data=valid_gene,
                    validation_steps=len(valid_arr) - num_steps,
                    callbacks=[checkpointer])
