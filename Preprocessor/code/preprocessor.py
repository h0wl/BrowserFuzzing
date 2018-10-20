# coding:utf8
import os
import re
import subprocess
from db_operation import *
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


def format_code(text):
    while text.__contains__('\n\n'):
        text = text.replace('\n\n', '\n')

    while text.__contains__('  '):
        text = text.replace('  ', ' ')
    return re.sub('[\n\t][\r ]*?[\n\t]', '\n', text)


def pre_process(text):
    text = remove_title(text)
    text = remove_comments_1(text)
    text = remove_comments_2(text)
    text = remove_comments_3(text)
    text = format_code(text)
    return text.strip('\n\t')


def uglify_js(file_name, corpus_path):
    """
    通过uglifyjs对JS语料库进行预处理，包括去注释、变量名替换、压缩
    遇到有语法错误的文件会报错，利用这个特性删除包含语法错误的代码
    """

    file_path = corpus_path + '/' + file_name
    cmd = ['uglifyjs', file_path, '-o', file_path, '-m', '-b']
    # p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
    # 下面这行注释针对Windows本地
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    if ((p.poll() is None) and p.stderr.readline() and os.path.exists(file_path)) or not os.path.getsize(file_path):
        os.remove(file_path)
        print('File \'' + file_name + '\' Contains Syntax Error or Content Is Empty. Been Deleted.')
        return 1
    return 0


def execute_pre_process():
    """
    遍历指定的语料库，执行预处理操作
    """

    # 拼装语料库路径
    corpus_path = FLAGS.corpus_folder + FLAGS.file_type
    # 如果文件夹不存在，创建
    if not os.path.exists(corpus_path):
        os.mkdir(corpus_path)

    print('----------------------- Executing Pre-Process -----------------------')

    file_count = 0
    counter = 0
    illegal_counter = 0
    if os.path.isdir(corpus_path):
        for root, dirs, files in os.walk(corpus_path):
            # 统计语料库中源文件个数
            file_count = files.__len__()
            # 如果本次预处理是对js文件执行
            if FLAGS.file_type.__eq__('js'):
                for file in files:
                    counter += 1
                    print('processing: ' + str(counter))
                    illegal_counter += uglify_js(file, corpus_path)
                print(str(illegal_counter) + ' Illegal JavaScript Files Has Been Removed.')
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
        print('Execute Pre-Process Finished on ' + str(file_count) + ' ' + FLAGS.file_type + ' Files.')
    else:
        print('\'' + corpus_path + '\' is not a directory.')


def write_corpus_to_db():
    """
    将语料写入数据库
    """
    # 拼装数据库文件路径
    db_path = FLAGS.db_folder + FLAGS.file_type + '_corpus.db'

    if not os.path.exists(db_path):
        init_db(db_path)

    # 拼装语料库路径
    corpus_path = FLAGS.corpus_folder + FLAGS.file_type
    # 如果文件夹不存在，创建
    if not os.path.exists(corpus_path):
        os.mkdir(corpus_path)

    print('----------------------- Executing Write Corpus to DB -----------------------')

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
                    with open(corpus_path + '/' + file, 'rb') as f:
                        insert(counter, f.read())
        print('Execute Write Corpus to DB on ' + str(file_count) + ' ' + FLAGS.file_type + ' Files.')
    else:
        print('\'' + corpus_path + '\' is not a directory.')


if __name__ == '__main__':
    FLAGS = tf.flags.FLAGS
    tf.flags.DEFINE_string('file_type', 'js', 'File type of current execution.')
    tf.flags.DEFINE_string('corpus_folder', '../../../BrowserFuzzingData/result/', 'Path of Corpus Folder')
    tf.flags.DEFINE_string('db_folder', '../../../BrowserFuzzingData/db/', 'Path of Corpus Folder')
    execute_pre_process()
    write_corpus_to_db()
