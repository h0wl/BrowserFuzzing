# coding:utf8
import os
import re
import subprocess


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


def mangle(file_path):
    """
    js预处理，包括去注释、变量名替换、压缩后再美化
    """

    file_abspath = os.path.abspath(file_path)
    cmd = ['uglifyjs', file_abspath, '-o', file_abspath, '-m', '-b']
    p = subprocess.Popen(cmd, cwd='/home/gxy/BrowserFuzzing/UglifyJS2/bin')
    p.wait()


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
