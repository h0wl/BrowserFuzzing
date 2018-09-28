# coding:utf8
import re


def removeTitle(text):
    return re.sub('<title[\\s\\S]*?title>', '', text)


def removeComments1(text):
    return re.sub('<!--[\\s\\S]*?-->', '', text)


def removeComments2(text):
    return re.sub('//[\\s\\S]*?[\n\t]', '', text)


def removeComments3(text):
    return re.sub('/\\*\\*[\\s\\S]*?\\*/', '', text)


def formate(text):
    return re.sub('[\n\t][\\s]*?[\n\t]', '\n', text)


def execute(text):
    text = removeTitle(text)
    text = removeComments1(text)
    text = removeComments2(text)
    text = removeComments3(text)
    text = formate(text)
    return text


if __name__ == '__main__':
    text = '/**\n' + \
           ' * 去除形如<!--comment-->这样的注释\n' \
           + ' *\n' \
           + ' * @param text 代码文本\n' \
           + ' * @return 处理后的代码文本\n' \
           + ' */' \
           + '<!DOCTYPE asdasdasdasda>' \
           + '// adujgahskdhaksda \n' \
           + '</script>\n' \
           + '    <!-- 代码部分end -->\n' \
           + '</body>' \
           + '<!--dasd-->' \
           + '/**\n\t  \t\n' \
           + ' * 去除形如<!--comment-->这样的注释\n' \
           + ' *\n' \
           + ' * @param text 代码文本\n' \
           + ' * @return 处理后的代码文本\n' \
           + ' */\n' \
           + '// comment \n'
    text = execute(text)
    print(text)
