# coding:utf8

'''

输入一个仓库(文件夹路径)

1. 提取其中的html，js，css文件

2. 变量替换 href，src等引用部分 以及 script片段 (用任意变量名替换)

'''

import shutil
import sys
import os
import re


# 输入仓库路径，返回所有文件的绝对路径（二维list），list[0]是文件名，list[1]是文件路径
import time


def get_html_css_js_files(repo_path):
    html_files = []
    css_files = []
    js_files = []

    html_pattern = '\.html$'
    css_pattern = '\.css$'
    js_pattern = '\.js$'

    if os.path.isdir(repo_path):  # 判断repo_path是否是一个文件夹
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                r = re.compile(html_pattern).findall(file)
                if len(r) != 0:
                    abs_file_path = os.path.join(root, file)
                    html_files.append([file, abs_file_path])

            for file in files:
                r = re.compile(css_pattern).findall(file)
                if len(r) != 0:
                    abs_file_path = os.path.join(root, file)
                    css_files.append([file, abs_file_path])

            for file in files:
                r = re.compile(js_pattern).findall(file)
                if len(r) != 0:
                    abs_file_path = os.path.join(root, file)
                    js_files.append([file, abs_file_path])
    else:
        print('[!] dir path error. ')
    return html_files, css_files, js_files


# 输入文件路径的二维list，将它们移至目标文件夹target_dir
def shift_file(file_list, target_dir):
    if os.path.isdir(target_dir):
        for file_name, file_path in file_list:
            shutil.copyfile(file_path, target_dir + '/' + file_name)


# 输入文件路径的二维list，将其中所有文件的引用部分和script片段替换为任意变量
def replace_quote(file_list):
    html_pat = '\.html$'  # 正则判断是否为html文件

    all_pat = '=".*?\.!(js|png|jpg|gif)"|=\'.*?\.!(js|png|jpg|gif)\''
    js_pat = '=".*?\.js"|=\'.*?\.js\'|=.*?\.js '  # 正则替换js
    pic_pat = '=".*?\.(png|jpg|gif)"|=\'.*?\.(png|jpg|gif)\'|=.*?\.(png|jpg|gif) '  # 正则替换图片
    script_pat = '<script>.*?</script>'  # 正则替换script脚本

    for f_name, f_path in file_list:

        r = re.compile(html_pat).findall(f_path)
        if len(r) != 0:  # 是.html文件
            with open(f_path, 'r') as html_file:
                text = re.compile(js_pat, re.S).sub('="a.js"', html_file.read())
                text = re.compile(pic_pat, re.S).sub('="b.png"', text)
                text = re.compile(script_pat, re.S).sub('<script>//script fragment</script>', text)  # 替换script片段为空
                text = re.compile(all_pat, re.S).sub('="abc"', text)

            with open(f_path, 'w') as html_file:
                html_file.write(text)


def xhelp():
    print("[*] -d, --repo_dir       要提取html,css,js的目录路径    <> 如 './ddd_dir'")
    print("[*] -o, --output_dir     结果输出文件夹                 <> 默认'./result'")
    print("[*] -h, --help           help帮助                       <> print this help")
    print("[*] Example : python hcj_sep.py -d '320andup-master'")
    sys.exit(1)


if __name__ == '__main__':
    start = time.clock()
    repo_path = '../BrowserFuzzingData/repositories'
    output_dir = '../BrowserFuzzingData/result'  # 输出目录

    try:
        for argv in sys.argv:
            if argv.lower() == "-d" or argv.lower() == "--repo_dir":
                repo_path = sys.argv[sys.argv.index(argv) + 1]
            elif argv.lower() == "-o" or argv.lower() == "--output_dir":
                output_dir = sys.argv[sys.argv.index(argv) + 1]
            elif argv.lower() == "-h" or argv.lower() == "--help":
                xhelp()
    except SystemExit:
        print("[!] Cheak your parametars input")
        sys.exit(0)
    except Exception:
        xhelp()

    if not os.path.exists(output_dir):  # 若文件不存在则新建文件夹
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    if not os.path.exists(output_dir + "/html"):  # 若文件不存在则新建文件夹
        os.makedirs(output_dir + "/html")

    if not os.path.exists(output_dir + "/css"):  # 若文件不存在则新建文件夹
        os.makedirs(output_dir + "/css")

    if not os.path.exists(output_dir + "/js"):  # 若文件不存在则新建文件夹
        os.makedirs(output_dir + "/js")

    html_files, css_files, js_files = get_html_css_js_files(repo_path)  # 得到目标文件夹的htmljscss文件路径
    shift_file(html_files, output_dir + "/html")  # 复制文件到新目录下
    shift_file(css_files, output_dir + "/css")  # 复制文件到新目录下
    shift_file(js_files, output_dir + "/js")  # 复制文件到新目录下
    html_files, css_files, js_files = get_html_css_js_files(output_dir)  # 获取新目录下的文件路径
    replace_quote(html_files)  # 变量替换新文件
    replace_quote(css_files)  # 变量替换新文件
    replace_quote(js_files)  # 变量替换新文件

    end = time.clock()
    print (end - start)
