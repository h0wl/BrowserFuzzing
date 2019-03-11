# coding:utf8
import os
import re
import shutil
import subprocess
import sys
import uuid
import tensorflow as tf

from db_operation import DBOperation
from callable_processor import CallableProcessor


class PostProcessor:
    def __init__(self, data_folder, raw_folder, db_folder, format=True, compress=False, mangle=False, remove_if_files_exist=True):
        self.data_folder = data_folder
        self.raw_folder = raw_folder
        self.db_folder = db_folder
        self.job_name = self.get_job_name()
        self.format = format
        self.compress = False if self.format else compress
        self.mangle = mangle
        self.remove_if_files_exist = remove_if_files_exist

    def get_job_name(self):
        tmp = self.raw_folder.split('/')
        return tmp.__getitem__(tmp.__len__() - 1)

    def generate_pure_correct_callables(self):
        print('Step 1 --> Initial Filtration: ')
        if not self.initial_filtration():
            return

        print('Step 2 --> Write Files to DB: ')
        if not self.write_files_to_db():
            return

        print('Step 3 --> Functionize: ')
        if not self.functionize():
            return

        print('Step 4 --> Redistribute: ')
        if not self.redistribute():
            return

        print('Step 5 --> Final Filtration: ')
        if not self.final_filtration():
            return

    def initial_filtration(self):
        """
        遍历指定的语料库，执行预处理操作
        """

        counter = 0
        illegal_counter = 0
        if os.path.exists(self.raw_folder) and os.path.isdir(self.raw_folder):
            for root, dirs, files in os.walk(self.raw_folder):
                # 如果本次预处理是对js文件执行
                for file in files:
                    counter += 1
                    progress = "\rProcessing: %d --> %s" % (counter, file)
                    sys.stdout.write(progress)
                    file_path = self.raw_folder + '/' + file
                    if self.syntax_check(file_path):
                        illegal_counter += 1
                        os.remove(file_path)
            counter += 0
            print('\rExecute Initial Filtration Finished on ' + str(counter) + ' Raw Files.')
            print(str(illegal_counter) + ' Illegal Ones Has Been Removed.')
            return True
        else:
            print('\'' + self.raw_folder + '\' Is Not A Directory.')
            return False

    def write_files_to_db(self):
        """
        将语料写入数据库
        """

        # 拼装语料库路径
        corpus_path = self.raw_folder
        # 如果文件夹不存在，报错并提前结束
        if not os.path.exists(corpus_path):
            print('Error: \'' + corpus_path + '\' is not exist! Check and do the last step again.')
            return False

        # 拼装数据库文件路径
        db_path = self.db_folder + '/js_corpus_initial_filtrated_' + self.job_name + '.db'
        db_op = DBOperation(db_path, 'corpus')
        if self.remove_if_files_exist:
            if os.path.exists(db_path):
                os.remove(db_path)
            db_op.init_db()
        elif not os.path.exists(db_path):
            db_op.init_db()

        counter = 0
        if os.path.isdir(corpus_path):
            for root, dirs, files in os.walk(corpus_path):
                # 如果本次预处理是对js文件执行
                for file in files:
                    try:
                        counter += 1
                        progress = "\rProcessing: %d --> %s" % (counter, file)
                        sys.stdout.write(progress)
                        f = open(corpus_path + '/' + file, 'rb')
                        db_op.insert(f.read().decode())
                        f.close()
                    except Exception:
                        pass
            counter += 0
            print('\rExecute Writing Content to DB Finished on ' + str(counter) + ' Files.')
            return True
        else:
            print('\'' + corpus_path + '\' Is Not A Directory.')
            return False

    def functionize(self):
        source_db_path = self.db_folder + '/js_corpus_initial_filtrated_' + self.job_name + '.db'
        if not os.path.exists(source_db_path):
            print('Error: \'' + source_db_path + '\' is not exist! Check and do the last step again.')
            return False

        target_db_path = self.db_folder + '/js_corpus_functionized_' + self.job_name + '.db'
        source_db_op = DBOperation(source_db_path, 'corpus')
        target_db_op = DBOperation(target_db_path, 'corpus')
        if self.remove_if_files_exist:
            if os.path.exists(target_db_path):
                os.remove(target_db_path)
            target_db_op.init_db()
        elif not os.path.exists(target_db_path):
            target_db_op.init_db()

        raws = source_db_op.query_all()

        counter = 0
        for raw in raws:
            counter += 1
            progress = "\rProcessing Raw No.%d" % counter
            sys.stdout.write(progress)
            raw = raw.__getitem__(0)
            if raw.__contains__('function'):
                self.extract_function(raw, target_db_op)
        target_size = target_db_op.query_count().__getitem__(0)
        counter += 0
        print('\rExecute Functionizing Finished. Extracted ' + str(target_size) + ' Functions From ' + str(
            counter) + ' Raws.')
        return True

    def redistribute(self):
        db_path = self.db_folder + '/js_corpus_functionized_' + self.job_name + '.db'
        if not os.path.exists(db_path):
            print('Error: \'' + db_path + '\' is not exist! Check and do the last step again.')
            return False

        db_op = DBOperation(db_path, "corpus")
        callables = db_op.query_all()
        target_path = self.data_folder + '/js_corpus_redistributed_' + self.job_name
        if self.remove_if_files_exist:
            if os.path.exists(target_path):
                os.remove(target_path)
            os.mkdir(target_path)
        elif not os.path.exists(target_path):
            os.mkdir(target_path)

        counter = 0
        for callable in callables:
            counter += 1
            progress = "\rProcessing: %d" % counter
            sys.stdout.write(progress)
            content = callable.__getitem__(0).decode('utf-8')
            if re.findall('function[\s\S]*?\(', content).__len__() > 0:
                re.sub('function[\s\S]*?\(', 'function(', content, 1)
            content = 'var a = ' + content
            file_name = uuid.uuid4().__str__() + '.js'
            try:
                self.create_file(target_path + '/' + file_name, content)
            except Exception:
                pass
        counter += 0
        print('\rExecute Redistribution Finished on ' + str(counter) + ' Files')
        return True

    def final_filtration(self):
        source_path = self.data_folder + '/js_corpus_redistributed_' + self.job_name
        if not os.path.exists(source_path):
            print('Error: \'' + source_path + '\' is not exist! Check and do the last step again.')
            return False

        db_path = self.db_folder + '/js_corpus_final_filtrated_' + self.job_name + '.db'
        db_op = DBOperation(db_path, "corpus")
        if self.remove_if_files_exist:
            if os.path.exists(db_path):
                os.remove(db_path)
            db_op.init_db()
        elif not os.path.exists(db_path):
            db_op.init_db()

        counter = 0
        if os.path.isdir(source_path):
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    counter += 1
                    progress = "\rProcessing: %d --> %s" % (counter, file)
                    sys.stdout.write(progress)
                    if self.syntax_check(source_path + '/' + file):
                        with open(source_path + '/' + file, 'r') as f:
                            file_content = f.read().replace('var a = ', '', 1)
                            db_op.insert(file_content.encode('utf-8'))
            counter += 0
            print('\rExecute Final Filtration Finished on ' + str(counter) + ' Files')
            return True
        else:
            print('\'' + source_path + '\' Is Not A Directory.')
            return False

    def syntax_check(self, file_path):
        """
        通过uglifyjs对JS语料库进行预处理，包括去注释、变量名替换、压缩
        遇到有语法错误的文件会报错，利用这个特性删除包含语法错误的代码
        """
        cmd = ['uglifyjs', file_path, '-o', file_path]
        if self.format:
            cmd.append('-b')
        elif self.compress:
            cmd.append('-c')
        if self.mangle:
            cmd.append('-m')

        p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        # 下面这行注释针对Windows本地
        # p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        if ((p.poll() is None) and p.stderr.readline() and os.path.exists(file_path)) or not os.path.getsize(
                file_path):
            return False
        return True

    def extract_function(self, file_content, op):
        index = 0

        while index < file_content.__len__():
            function_index = file_content.find('function', index)
            if function_index > -1:
                function_body = ''
                while function_index < file_content.__len__() and file_content[function_index] != '{':
                    function_body += file_content[function_index]
                    function_index += 1
                function_body += '{'
                function_index += 1

                open_brace = 1
                close_brace = 0
                while function_index < file_content.__len__() and open_brace != close_brace:
                    current_character = file_content[function_index]
                    function_body += current_character
                    if current_character == '{':
                        open_brace += 1
                    if current_character == '}':
                        close_brace += 1
                    function_index += 1
                function_body += ';'
                index = function_index + 1
                if function_body.__contains__('function'):
                    function_body = re.sub('function [\s\S]*?\(', 'function(', function_body, 1)
                    op.insert(function_body.encode())
            else:
                break

    def create_file(self, filename, file_content):
        file = open(filename, 'a')
        file.write(file_content)
        file.close()


def move_file(source, target):
    shutil.move(source, target)


def uglify_js(file_name, generated_path):
    """
    通过uglifyjs对JS语料库进行预处理，包括去注释、变量名替换、压缩
    遇到有语法错误的文件会报错，利用这个特性删除包含语法错误的代码
    """

    file_path = generated_path + '/' + file_name
    cmd = ['uglifyjs', file_path, '-o', file_path, '-b']
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
    # 下面这行注释针对Windows本地
    # p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    if not os.path.getsize(file_path):
        os.remove(file_path)

    if os.path.exists(file_path) and (p.poll() is None) and p.stderr.readline():
        move_file(file_path, generated_path + '_bad/' + file_name)


def sorting_by_syntax_checking():
    """
    遍历指定的语料库，执行预处理操作
    """

    # 拼装语料库路径
    generated_path = FLAGS.generated_folder + FLAGS.file_type
    # 如果文件夹不存在，创建
    if not os.path.exists(generated_path):
        os.mkdir(generated_path)

    if not os.path.exists(generated_path + '_bad'):
        os.mkdir(generated_path + '_bad')

    print('----------------------- Executing Sort by Syntax Checking -----------------------')

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
                    progress = "\rProcessing: %d -> %s" % (counter, file)
                    sys.stdout.write(progress)
                    uglify_js(file, generated_path)
        print('\nExecute Sort by Syntax Checking Finished on ' + str(file_count) + ' ' + FLAGS.file_type + ' Files')
    else:
        print('\'' + generated_path + '\' is not a directory.')


def sorting_by_callable_checking():
    sorted_path = FLAGS.generated_folder + FLAGS.file_type

    if not os.path.exists(sorted_path + '_callable'):
        os.mkdir(sorted_path + '_callable')

    print('----------------------- Executing Sort by Callable Checking -----------------------')

    file_count = 0
    counter = 0
    if os.path.isdir(sorted_path):
        for root, dirs, files in os.walk(sorted_path):
            # 统计语料库中源文件个数
            file_count = files.__len__()
            # 如果本次预处理是对js文件执行
            if FLAGS.file_type.__eq__('js'):
                for file in files:
                    counter += 1
                    progress = "\rProcessing: %d -> %s" % (counter, file)
                    sys.stdout.write(progress)
                    with open(sorted_path + '/' + file, 'r') as f:
                        file_content = f.read()
                        f.close()
                        if file_content.__contains__('function'):
                            move_file(sorted_path + '/' + file, sorted_path + '_callable/' + file)
        print('\nExecute Sort by Callable Checking Finished on ' + str(file_count) + ' ' + FLAGS.file_type + ' Files')
    else:
        print('\'' + sorted_path + '\' is not a directory.')


# def generate_js_fuzzer(raw_callables, function_body):
#     callable_processor = CallableProcessor(raw_callables)
#     try:
#         self_calling = callable_processor.get_a_self_calling(function_body)
#         file_name = uuid.uuid1().__str__() + '.js'
#         create_file(file_name, self_calling)
#     except Exception:
#         pass
#
# def check_coverage():
#     result = [0, 0, 0, 0]
#     covered = [0, 0, 0, 0]
#     total = [0, 0, 0, 0]
#     source_path = './'
#
#     file_count = 0
#     counter = 0
#     if os.path.isdir(source_path):
#         for root, dirs, files in os.walk(source_path):
#             if dirs.__contains__('.idea'):
#                 dirs.remove('.idea')
#             if dirs.__contains__('coverage'):
#                 dirs.remove('coverage')
#             if dirs.__contains__('__pycache__'):
#                 dirs.remove('__pycache__')
#             if files.__contains__('callable_processor.py'):
#                 files.remove('callable_processor.py')
#             if files.__contains__('db_operation.py'):
#                 files.remove('db_operation.py')
#             if files.__contains__('postprocessor.py'):
#                 files.remove('postprocessor.py')
#             if files.__contains__('serializer.py'):
#                 files.remove('serializer.py')
#             if files.__contains__('callable_processor.pyc'):
#                 files.remove('callable_processor.pyc')
#             if files.__contains__('db_operation.pyc'):
#                 files.remove('db_operation.pyc')
#             if files.__contains__('postprocessor.pyc'):
#                 files.remove('postprocessor.pyc')
#             if files.__contains__('serializer.pyc'):
#                 files.remove('serializer.pyc')
#
#             # 统计语料库中源文件个数
#             file_count = files.__len__()
#             print(file_count)
#             # 如果本次预处理是对js文件执行
#             correct_count = 0
#             for file in files:
#                 counter += 1
#                 progress = "\rProcessing: %d -> %s\n" % (counter, file)
#                 sys.stdout.write(progress)
#                 cmd = ['istanbul', 'cover', file]
#                 p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#
#                 p.poll()
#                 stdout_list = p.stdout.readlines()
#                 stdout = ''
#                 for line in stdout_list:
#                     stdout = stdout + line.decode('utf-8')
#                 coverage_of_single_sample = re.findall(': [\s\S]*?%', stdout)
#                 covered_of_single_sample = re.findall('\( [\s\S]*?/', stdout)
#                 total_of_single_sample = re.findall('/[\s\S]*? \)', stdout)
#                 if coverage_of_single_sample.__len__() == 4:
#                     for i in range(0, 4):
#                         ce = re.sub('%', '', re.sub(': ', '', coverage_of_single_sample[i]))
#                         result[i] += float(ce)
#                         cd = re.sub('\( ', '', re.sub('/', '', covered_of_single_sample[i]))
#                         covered[i] += int(cd)
#                         tl = re.sub(' \)', '', re.sub('/', '', total_of_single_sample[i]))
#                         total[i] += int(tl)
#                     correct_count += 1
#
#                 print('Analize Finished on ' + str(correct_count) + ' Files')
#                 print('Mean Statement Coverage: ' + str(result[0] / correct_count) + ' (' + str(covered[0]) + '/' + str(
#                     total[0]) + ')')
#                 print('Mean Branch Coverage: ' + str(result[1] / correct_count) + ' (' + str(covered[1]) + '/' + str(
#                     total[1]) + ')')
#                 print('Mean Function Coverage: ' + str(result[2] / correct_count) + ' (' + str(covered[2]) + '/' + str(
#                     total[2]) + ')')
#                 print('Mean Line Coverage: ' + str(result[3] / correct_count) + ' (' + str(covered[3]) + '/' + str(
#                     total[3]) + ')')


if __name__ == '__main__':
    FLAGS = tf.flags.FLAGS
    tf.flags.DEFINE_string('file_type', 'js', 'File type of current execution.')
    tf.flags.DEFINE_string('data_folder', '../../BrowserFuzzingData', 'Path of Data Folder')
    tf.flags.DEFINE_string('raw_folder', '../../BrowserFuzzingData/test', 'Path of Corpus Folder')
    tf.flags.DEFINE_string('db_folder', '../../BrowserFuzzingData/db', 'Path of Corpus Folder')
    post_processor = PostProcessor(FLAGS.data_folder, FLAGS.raw_folder, FLAGS.db_folder)
    post_processor.generate_pure_correct_callables()
