# coding:utf8

import os
import numpy as np
import tensorflow as tf

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

chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
         'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '~', '!', '@', '#',
         '$', '%', '^', '&', '*', '(', ')', '-', '+', '_', '=', '[', ']', '{', '}', ';', ':', '\'', '"', ',', '.', '<',
         '>', '/', '?', '\\', '|', '`', ' ', '\n', '\r']


def read_corpus(repository_path):
    if os.path.isdir(repository_path):
        for root, dirs, files in os.walk(repository_path):  # 遍历目录
            for file in files:  # 遍历当前文件
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    file_content = str(f.read())
                    corpus.append(file_content)
    else:
        print(repository_path + ' is not an directory !')


# ---------------------------------------RNN--------------------------------------#
# 定义RNN
def neural_network(rnn_size=128, num_layers=2):
    cell = tf.nn.rnn_cell.LSTMCell(rnn_size, state_is_tuple=True)
    cell = tf.nn.rnn_cell.MultiRNNCell([cell] * num_layers, state_is_tuple=True)

    initial_state = cell.zero_state(batch_size, tf.float32)

    # with tf.variable_scope('rnnlm'):
    with tf.device("/cpu:0"):
        inputs = tf.nn.embedding_lookup(tf.get_variable("embedding", [len(tokenSet), rnn_size]), input_data)

    outputs, last_state = tf.nn.dynamic_rnn(cell, inputs, initial_state=initial_state, scope='rnnlm')
    output = tf.reshape(outputs, [-1, rnn_size])

    logits = tf.matmul(output, tf.get_variable("softmax_w", [rnn_size, len(tokenSet)])) + tf.get_variable(
        "softmax_b", [len(tokenSet)])
    probs = tf.nn.softmax(logits)
    return logits, last_state, probs, cell, initial_state


# -------------------------------生成代码---------------------------------#
# 使用训练完成的模型

def gen_poetry():
    def to_word(weights):
        t = np.cumsum(weights)
        s = np.sum(weights)
        sample = int(np.searchsorted(t, np.random.rand(1) * s))
        return tokenSet[sample]

    _, last_state, probs, cell, initial_state = neural_network()

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        saver = tf.train.Saver(tf.global_variables())
        saver.restore(sess, 'C:/Users/Implementist/Desktop/BrowserFuzzingData/result/js.module-49')

        state_ = sess.run(cell.zero_state(1, tf.float32))

        x = np.array([list(map(dictionary.get, '['))])
        [probs_, state_] = sess.run([probs, last_state], feed_dict={input_data: x, initial_state: state_})
        word = to_word(probs_)
        # word = words[np.argmax(probs_)]
        code = ''
        while word != ']':
            code += word
            x = np.zeros((1, 1))
            x[0, 0] = dictionary[word]
            [probs_, state_] = sess.run([probs, last_state], feed_dict={input_data: x, initial_state: state_})
            word = to_word(probs_)
        # word = words[np.argmax(probs_)]
        return code


# Each item of corpus is content of a file
corpus = []

# Train 64 files together on each time
batch_size = 1

input_data = tf.placeholder(tf.int32, [batch_size, None])
output_targets = tf.placeholder(tf.int32, [batch_size, None])
if __name__ == '__main__':
    tokenSet = js_tokens + chars
    dictionary = dict(zip(tokenSet, range(len(tokenSet))))

    repository_path = "C:/Users/Implementist/Desktop/BrowserFuzzingData/result/js"
    # Read file content from corpus
    print("-------------------------Reading Corpus-------------------------")
    read_corpus(repository_path)
    print("Read Out " + str(corpus.__len__()) + " Files From Corpus")

    print("-------------------------Generating-------------------------")

    print("Code : " + gen_poetry())
