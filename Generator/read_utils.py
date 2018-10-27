import copy
import pickle
import time

import numpy as np
from db_operation import query_all


def batch_generator(arr, n_seqs, n_steps):
    arr = copy.copy(arr)
    batch_size = n_seqs * n_steps
    n_batches = int(len(arr) / batch_size)
    arr = arr[:batch_size * n_batches]
    arr = arr.reshape((n_seqs, -1))
    while True:
        np.random.shuffle(arr)
        for n in range(0, arr.shape[1], n_steps):
            x = arr[:, n:n + n_steps]
            y = np.zeros_like(x)
            y[:, :-1], y[:, -1] = x[:, 1:], x[:, 0]
            yield x, y


def read_corpus():
    global training_corpus, validating_corpus
    training_corpus = ''
    validating_corpus = ''
    print("---------------------------- Reading Corpus ----------------------------")
    start_time = time.time()
    source_list = list(query_all())
    print("Read Corpus Finished in " + str(time.time() - start_time) + ' Seconds.')

    training_corpus_percentage = 0.9
    training_corpus_length = int(len(source_list) * training_corpus_percentage) + 1

    print("---------------------------- Building Training Data Set ----------------------------")
    start_time = time.time()
    training_corpus = '\n'.join(v.__getitem__(0) for v in source_list[0:training_corpus_length])
    print("Build Training Data Set Finished in " + str(time.time() - start_time) + ' Seconds.')

    print("---------------------------- Building Validating Data Set ----------------------------")
    start_time = time.time()
    validating_corpus = '\n'.join(v.__getitem__(0) for v in source_list[training_corpus_length:len(source_list)])
    print("Build Validating Data Set Finished in " + str(time.time() - start_time) + " Seconds.")
    return training_corpus, validating_corpus


def vectroize_corpus(converter):
    print("---------------------------- Vectorizing Corpus ----------------------------")
    start_time = time.time()
    global training_vector_array, validating_vector_array
    training_vector_array = converter.text_to_arr(training_corpus)
    validating_vector_array = converter.text_to_arr(validating_corpus)
    print("Vectorize Corpus Finished in " + str(time.time() - start_time) + " Seconds.")


def get_batch_generator(_type_, num_seqs, num_steps):
    if _type_ == 'training':
        return batch_generator(training_vector_array, num_seqs, num_steps)
    else:
        return batch_generator(validating_vector_array, num_seqs, num_steps)


class TextConverter(object):
    def __init__(self, text=None, max_vocab=5000, filename=None):
        if filename is not None:
            with open(filename, 'rb') as f:
                self.vocab = pickle.load(f)
        else:
            vocab = set(text)
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

    def text_to_arr(self, text):
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
