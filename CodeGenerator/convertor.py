import copy
import pickle

import numpy as np

js_tokens = ['abstract', 'arguments', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const',
             'continue', 'debugger', 'default', 'delete', 'do', 'double', 'else', 'enum', 'eval', 'export',
             'extends', 'false', 'final', 'finally', 'float', 'for', 'function', 'goto', 'if', 'implements',
             'import', 'in', 'instanceof', 'int', 'interface', 'let', 'long', 'native', 'new', 'null', 'package',
             'private', 'protected', 'public', 'return', 'short', 'static', 'super', 'switch', 'synchronized',
             'this', 'throw', 'throws', 'transient', 'true', 'try', 'typeof', 'var', 'void', 'volatile', 'while',
             'with', 'yield', 'Array', 'Date', 'eval', 'function', 'hasOwnProperty', 'Infinity', 'isFinite', 'isNaN',
             'isPrototypeOf', 'length', 'Math', 'NaN', 'name', 'Number', 'Object', 'prototype', 'String', 'toString',
             'undefined', 'valueOf', 'getClass', 'java', 'JavaArray', 'javaClass', 'JavaObject', 'JavaPackage',
             'alert', 'all', 'anchor', 'anchors', 'area', 'assign', 'blur', 'button', 'checkbox', 'clearInterval',
             'clearTimeout', 'clientInformation', 'close', 'closed', 'confirm', 'constructor', 'crypto', 'decodeURI',
             'decodeURIComponent', 'defaultStatus', 'document', 'element', 'elements', 'embed', 'embeds', 'encodeURI',
             'encodeURIComponent', 'escape', 'event', 'fileUpload', 'focus', 'form', 'forms', 'frame', 'innerHeight',
             'innerWidth', 'layer', 'layers', 'link', 'location', 'mimeTypes', 'navigate', 'navigator', 'frames',
             'frameRate', 'hidden', 'history', 'image', 'images', 'offscreenBuffering', 'open', 'opener', 'option',
             'outerHeight', 'outerWidth', 'packages', 'pageXOffset', 'pageYOffset', 'parent', 'parseFloat', 'parseInt',
             'password', 'pkcs11', 'plugin', 'prompt', 'propertyIsEnum', 'radio', 'reset', 'screenX', 'screenY',
             'scroll', 'secure', 'select', 'self', 'setInterval', 'setTimeout', 'status', 'submit', 'taint', 'text',
             'textarea', 'top', 'unescape', 'untaint', 'window', 'onblur', 'obclick', 'onerror', 'onfocus', 'onkeydown',
             'onkeypress', 'onkeyup', 'onmouseover', 'onload', 'onmouseup', 'onmousedown', 'onsubmit']


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


def count_word_frequency(vocab_count, text):
    try:
        temp_word = ""
        for char in text:
            if char.isdigit() | char.isalpha():
                temp_word += char
            else:
                if temp_word.__len__() != 0:
                    if tokenSet.__contains__(temp_word):
                        vocab_count[dictionary[temp_word]] += 1
                    else:
                        for c in temp_word:
                            vocab_count[dictionary[c]] += 1
                vocab_count[dictionary[char]] += 1
                temp_word = ""

        if temp_word.__len__() != 0:
            if tokenSet.__contains__(temp_word):
                vocab_count[dictionary[temp_word]] += 1
            else:
                for c in temp_word:
                    vocab_count[dictionary[c]] += 1
        return vocab_count
    except KeyError:
        pass


def vectorize(text):
    vector_of_text = []
    temp_word = ""
    for char in text:
        if char.isdigit() | char.isalpha():
            temp_word += char
        else:
            if temp_word.__len__() != 0:
                if tokenSet.__contains__(temp_word):
                    vector_of_text.append(dictionary[temp_word])
                else:
                    for c in temp_word:
                        vector_of_text.append(dictionary[c])
            vector_of_text.append(dictionary[char])
            temp_word = ""

    if temp_word.__len__() != 0:
        if tokenSet.__contains__(temp_word):
            vector_of_text.append(dictionary[temp_word])
        else:
            for c in temp_word:
                vector_of_text.append(dictionary[c])
    return vector_of_text


class TextConverter(object):
    def __init__(self, text=None, max_vocab=5000, filename=None):
        global tokenSet
        tokenSet = js_tokens + list(set(text))
        global dictionary
        dictionary = dict(zip(tokenSet, range(len(tokenSet))))

        if filename is not None:
            with open(filename, 'rb') as f:
                self.vocab = pickle.load(f)
        else:
            vocab = tokenSet
            # max_vocab_process
            vocab_count = {}
            for word in vocab:
                vocab_count[word] = 0
            vocab_count = count_word_frequency(vocab_count, text)
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
        vector_of_text = []
        temp_word = ""
        for char in text:
            if char.isdigit() | char.isalpha():
                temp_word += char
            else:
                if temp_word.__len__() != 0:
                    if tokenSet.__contains__(temp_word):
                        vector_of_text.append(dictionary[temp_word])
                    else:
                        for c in temp_word:
                            vector_of_text.append(dictionary[c])
                vector_of_text.append(dictionary[char])
                temp_word = ""

        if temp_word.__len__() != 0:
            if tokenSet.__contains__(temp_word):
                vector_of_text.append(dictionary[temp_word])
            else:
                for c in temp_word:
                    vector_of_text.append(dictionary[c])
        return np.array(vector_of_text)

    def arr_to_text(self, arr):
        words = []
        for index in arr:
            words.append(self.int_to_word(index))
        return "".join(words)

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.vocab, f)
