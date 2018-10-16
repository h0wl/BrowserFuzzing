# coding:utf8
import os
import re
import subprocess

import tensorflow as tf


def remove_title(text):
    """
    去除html文件的<title>标签
    """

    return re.sub('<title[\s\S]*?title>', '', text)


def remove_comments_1(text):
    """
    去除形如<!-- comments -->的单行注释
    """

    return re.sub('<!--[\s\S]*?-->', '', text)


def remove_comments_2(text):
    """
    去除形如// comments 的单行注释
    """

    text = text.replace('://', '<SpecialSymbol>')
    text = re.sub('//[\s\S]*?[\n\t]', '', text)
    return text.replace('<SpecialSymbol>', '://')


def remove_comments_3(text):
    """
    去除形如
    /*
     * comments
     */
     的块级注释
    """
    return re.sub('/\*[\s\S]*?\*/', '', text)


def mangle(file_name, corpus_path):
    """
    js预处理，包括去注释、变量名替换、压缩后再美化
    """

    file_abspath = os.path.abspath(corpus_path + '/' + file_name)
    cmd = ['uglifyjs', file_abspath, '-o', file_abspath, '-m']
    p = subprocess.Popen(cmd, cwd='/home/gxy/BrowserFuzzing/UglifyJS2/bin')
    p.wait()


def format_code(text):
    while text.__contains__('\n\n'):
        text = text.replace('\n\n', '\n')
    return re.sub('[\n\t][\r ]*?[\n\t]', '\n', text)


def pre_process(text):
    text = remove_title(text)
    text = remove_comments_1(text)
    text = remove_comments_2(text)
    text = remove_comments_3(text)
    text = format_code(text)
    return text.strip('\n\t')


def execute_pre_process():
    """
    遍历指定的语料库，执行预处理操作
    """

    # 拼装语料库路径
    corpus_path = '../../../BrowserFuzzingData/result/' + FLAGS.file_type
    print('----------------------- executing pre-process -----------------------')
    file_count = 0
    counter = 0
    if os.path.isdir(corpus_path):
        for root, dirs, files in os.walk(corpus_path):
            # 统计语料库中源文件个数
            file_count = files.__len__()
            # 如果本次预处理是对js文件执行
            if FLAGS.file_type.__eq__('js'):
                for file in files:
                    counter += 1
                    print('processing: ' + str(counter))
                    mangle(file, corpus_path)
            # 如果本次预处理是对html文件执行
            elif FLAGS.file_type.__eq__('html'):
                for file in files:
                    counter += 1
                    print('processing: ' + str(counter))
                    with open(corpus_path + '/' + file, 'r+') as f:
                        file_content = str(f.read())
                        file_content = pre_process(file_content)
                        f.write(file_content)
            # TODO: 这里留给css，暂时不执行任何动作
            else:
                pass
        print('execute pre-process finished on ' + str(file_count) + ' ' + FLAGS.file_type + ' files.')
    else:
        print('\'' + corpus_path + '\' is not a directory.')


if __name__ == '__main__':
    FLAGS = tf.flags.FLAGS
    tf.flags.DEFINE_string('file_type', 'js', 'File type of current execution.')
    execute_pre_process()
