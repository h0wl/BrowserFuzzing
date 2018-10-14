# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 06:14:13 2018
@author: xiaozhen
split the text to train, valid, test; as well, the space can be deleted
"""

with open('wonderland.txt', 'r', encoding='utf-8') as f:
    jay_file = f.read()

size = len(jay_file)
train_data = jay_file[:int(size * 0.7)]
vali_data = jay_file[int(size * 0.7):int(size * 0.9)]
test_data = jay_file[int(size * 0.9):]

for file, data in zip(["train.txt", "valid.txt", "test.txt"],
                      [train_data, vali_data, test_data]):
    with open(file, 'w', encoding='utf8') as f:
        f.write(data)
