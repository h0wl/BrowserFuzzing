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


def format_code(text):
    while text.__contains__('\n\n'):
        text = text.replace('\n\n', '\n')

    while text.__contains__('  '):
        text = text.replace('  ', ' ')
    return re.sub('[\n\t][\r ]*?[\n\t]', '\n', text)


def post_process(text):
    text = remove_title(text)
    text = remove_comments_1(text)
    text = remove_comments_2(text)
    text = remove_comments_3(text)
    text = format_code(text)
    return text.strip('\n\t')


def uglify_js(file_name, corpus_path):
    """
    通过uglifyjs对JS语料库进行预处理，包括去注释、变量名替换、美化
    因为要用于测试，因此不做语法检查
    """

    file_abspath = os.path.abspath(corpus_path + '/' + file_name)
    cmd = ['uglifyjs', file_abspath, '-o', file_abspath, '-m', '-b']
    # p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
    # 下面这行注释针对Windows本地
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    p.wait()


def execute_post_process():
    FLAGS = tf.flags.FLAGS
    # 拼装语料库路径
    generated_path = FLAGS.generated_folder + FLAGS.file_type
    # 如果文件夹不存在，创建
    if not os.path.exists(generated_path):
        os.mkdir(generated_path)

    print('----------------------- Executing Post-Process -----------------------')

    file_count = 0
    counter = 0
    if os.path.isdir(generated_path):
        for root, dirs, files in os.walk(generated_path):
            # 统计语料库中源文件个数
            file_count = files.__len__()
            # 如果本次预处理是对js文件执行
            if FLAGS.file_type.__eq__('js'):
                for file in files:
                    counter += 1
                    print('processing: ' + str(counter))
                    uglify_js(file, generated_path)
            # 如果本次预处理是对html文件执行
            elif FLAGS.file_type.__eq__('html'):
                for file in files:
                    counter += 1
                    print('processing: ' + str(counter))
                    with open(generated_path + '/' + file, 'r+') as f:
                        file_content = str(f.read())
                        file_content = post_process(file_content)
                        f.write(file_content)
            # TODO: 这里留给css，暂时不执行任何动作
            else:
                pass
        print('Execute Post-Process Finished on ' + str(file_count) + ' ' + FLAGS.file_type + ' Files.')
    else:
        print('\'' + generated_path + '\' is not a directory.')


# if __name__ == '__main__':
#     FLAGS = tf.flags.FLAGS
#     tf.flags.DEFINE_string('file_type', 'js', 'File Type of Current Progress')
#     tf.flags.DEFINE_string('generated_folder', '../../BrowserFuzzingData/generated/', 'Path of Generated Folder')
#     execute_post_process()
