# coding:utf8
import re


def remove_title(text):
    return re.sub('<title[\s\S]*?title>', '', text)


def remove_comments_1(text):
    return re.sub('<!--[\s\S]*?-->', '', text)


def remove_comments_2(text):
    text = text.replace('://', '<SpecialSymbol>')
    text = re.sub('//[\s\S]*?[\n\t]', '', text)
    return text.replace('<SpecialSymbol>', '://')


def remove_comments_3(text):
    return re.sub('/\*[\s\S]*?\*/', '', text)


def format_code(text):
    # TODO : Add uglifyjs calling to process generated js files.
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
