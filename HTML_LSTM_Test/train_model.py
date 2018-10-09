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
                    file_content = '[' + str(f.read()) + ']'
                    corpus.append(file_content)
    else:
        print(repository_path + ' is not an directory !')


def vectorize(content_of_corpus):
    global tokenSet
    tokenSet = js_tokens + chars
    global dictionary
    dictionary = dict(zip(tokenSet, range(len(tokenSet))))

    for item in content_of_corpus:
        try:
            verctor_of_item = []
            temp_word = ""
            for char in item:
                if char.isdigit() | char.isalpha():
                    temp_word += char
                else:
                    if temp_word.__len__() != 0:
                        if tokenSet.__contains__(temp_word):
                            verctor_of_item.append(dictionary[temp_word])
                        else:
                            for c in temp_word:
                                verctor_of_item.append(dictionary[c])
                    verctor_of_item.append(dictionary[char])
                    temp_word = ""

            if temp_word.__len__() != 0:
                if tokenSet.__contains__(temp_word):
                    verctor_of_item.append(dictionary[temp_word])
                else:
                    for c in temp_word:
                        verctor_of_item.append(dictionary[c])
            vectors.append(verctor_of_item)
        except KeyError:
            continue


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


# 训练
def train_neural_network():
    logits, last_state, _, _, _ = neural_network()
    targets = tf.reshape(output_targets, [-1])
    loss = tf.contrib.legacy_seq2seq.sequence_loss_by_example([logits], [targets],
                                                              [tf.ones_like(targets, dtype=tf.float32)],
                                                              len(corpus))
    cost = tf.reduce_mean(loss)
    learning_rate = tf.Variable(0.0, trainable=False)
    tvars = tf.trainable_variables()
    grads, _ = tf.clip_by_global_norm(tf.gradients(cost, tvars), 5)
    optimizer = tf.train.AdamOptimizer(learning_rate)
    train_op = optimizer.apply_gradients(zip(grads, tvars))

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        saver = tf.train.Saver(tf.global_variables())

        for epoch in range(50):
            sess.run(tf.assign(learning_rate, 0.002 * (0.97 ** epoch)))
            n = 0
            for batche in range(n_chunk):
                train_loss, _, _ = sess.run([cost, last_state, train_op],
                                            feed_dict={input_data: x_batches[n], output_targets: y_batches[n]})
                n += 1
                print(epoch, batche, train_loss)
            if epoch % 7 == 0:
                saver.save(sess, 'C:/Users/Implementist/Desktop/BrowserFuzzingData/result/js.module', global_step=epoch)


# Each item of corpus is content of a file
corpus = []
# Vectors of corpus.
vectors = []

# Train 64 files together on each time
batch_size = 1280
n_chunk = len(vectors) // batch_size
x_batches = []
y_batches = []

input_data = tf.placeholder(tf.int32, [batch_size, None])
output_targets = tf.placeholder(tf.int32, [batch_size, None])
if __name__ == '__main__':
    repository_path = "C:/Users/Implementist/Desktop/BrowserFuzzingData/result/js"
    # Read file content from corpus
    print("-------------------------Reading Corpus-------------------------")
    read_corpus(repository_path)
    print("Read Out " + str(corpus.__len__()) + " Files From Corpus")
    # Vectorize content of corpus.
    print("-------------------------Vectorizing-------------------------")
    vectorize(corpus)
    print("Vectorization Finished")

    for i in range(n_chunk):
        start_index = i * batch_size
        end_index = start_index + batch_size

        batches = vectors[start_index:end_index]
        length = max(map(len, batches))
        xdata = np.full((batch_size, length), dictionary[' '], np.int32)
        for row in range(batch_size):
            xdata[row, :len(batches[row])] = batches[row]
        ydata = np.copy(xdata)
        ydata[:, :-1] = xdata[:, 1:]
        """
        xdata             ydata
        [6,2,4,6,9]       [2,4,6,9,9]
        [1,4,2,8,5]       [4,2,8,5,5]
        """
        x_batches.append(xdata)
        y_batches.append(ydata)

    print("-------------------------Training-------------------------")
    train_neural_network()
    print("Train Finished")
