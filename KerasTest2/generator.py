import pickle

import matplotlib.pyplot as plt
import numpy as np
from keras import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.utils import to_categorical


def show_train_history(train_history, train, validation):
    plt.plot(train_history.history[train])
    plt.plot(train_history.history[validation])
    plt.title('Train History')
    plt.ylabel(train)
    plt.xlabel('Epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()


def batch_generator_one_word(arr, n_seqs, n_steps, vocab_size):
    batch_size = n_seqs * n_steps
    print(batch_size)
    n_batches = len(arr) // batch_size
    arr = arr[:batch_size * n_batches]

    while True:
        idx = 0
        while idx < len(arr) - n_steps - n_seqs - 1:
            train_x = []
            train_y = []
            for n in range(idx, idx + n_seqs):
                x = arr[n:(n + n_steps)]
                y = arr[n + n_steps + 1]
                train_x.append(x)
                train_y.append(y)
            idx += n_seqs
            train_x = np.array(train_x)
            train_y = to_categorical(train_y, num_classes=vocab_size)
            yield train_x, train_y


class TextConverter(object):
    def __init__(self, filename, max_vocab=None):
        with open(filename, 'r', encoding='utf8') as f:
            text = f.read()
        vocab = set(text)
        if not max_vocab:
            max_vocab = len(vocab)
        # max_vocab_process
        vocab_count = {}
        for word in vocab:
            vocab_count[word] = 0
        for word in text:
            vocab_count[word] += 1
        vocab_count_list = []
        for word in vocab_count:
            vocab_count_list.append((word, vocab_count[word]))
        vocab_count_list.sort(key=lambda x: x[1], reverse=True)
        if len(vocab_count_list) > max_vocab:
            vocab_count_list = vocab_count_list[:max_vocab]
        vocab = [x[0] for x in vocab_count_list]
        self.vocab = vocab
        self.text = text
        self.word_to_int_table = {c: i for i, c in enumerate(self.vocab)}
        self.int_to_word_table = dict(enumerate(self.vocab))

    @property
    def vocab_size(self):
        return len(self.vocab) + 1

    def word_to_int(self, word):
        if word in self.word_to_int_table:
            return self.word_to_int_table[word]
        else:
            return len(self.vocab)

    def int_to_word(self, index):
        if index == len(self.vocab):
            return '<unk>'
        elif index < len(self.vocab):
            return self.int_to_word_table[index]
        else:
            raise Exception('Unknown index!')

    def text_to_arr(self, text=None, filename=None):
        if filename:
            with open(filename, 'r', encoding='utf8') as f:
                text = f.read()
        arr = []
        for word in text:
            arr.append(self.word_to_int(word))
        return np.array(arr)

    def arr_to_text(self, arr):
        words = []
        for index in arr:
            words.append(self.int_to_word(index))
        return "".join(words)

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.vocab, f)


if __name__ == "__main__":
    num_steps = 32
    # 预测生成文本
    num_predict = 100
    convert_text = TextConverter(filename='wonderland.txt')
    test_arr = convert_text.text_to_arr(filename='predict.txt')
    vocab_size = convert_text.vocab_size
    model = Sequential()
    model.add(Embedding(output_dim=100,
                        input_dim=vocab_size,
                        input_length=num_steps))
    # model.add(Dropout(0.35))
    # units 是输出空间的维度
    model.add(LSTM(units=128, dropout=0.2, return_sequences=True))
    model.add(LSTM(units=128, dropout=0.2))
    model.add(Dense(units=vocab_size, activation='softmax'))
    model.load_weights('model-22.hdf5')
    for i in range(num_predict):
        startarr = np.array(test_arr[-num_steps:]).reshape(1, -1)
        pred_rst = model.predict(startarr)
        pred_idx = np.argmax(pred_rst[0])
        test_arr = np.append(test_arr, pred_idx)

    pred_text = convert_text.arr_to_text(test_arr)
    print(pred_text)
