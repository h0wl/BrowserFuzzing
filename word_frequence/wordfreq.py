# 匹配变量类型的方法
import os
import sys

from db_operation import DBOperation


class WordFreq:
    def __init__(self, methods, source_path, target_path):
        self.methods = methods
        self.columns = self.get_columns()
        self.db_op_source = DBOperation(source_path, 'corpus')
        self.db_op_target = DBOperation(target_path, "result")
        self.db_op_target.init_db()

    def frequence(self):
        # 切割文件形成一个字典
        file_name = 0  # 文件名起始值
        db_file_number = self.db_op_source.query_count()[0]  # 目录下文件的个数  592304
        callables = self.db_op_source.query_all()  # 返回所有的content
        count = 0  # 计数，最大为文件夹下文件的个数
        length = len(self.methods)  # 变量类型方法个数

        while count < db_file_number:
            file = ""
            file += callables[count][0].decode('utf-8')
            i = 0
            progress = "\rProcessing: %d" % file_name
            sys.stdout.write(progress)
            frequencies = []
            while i < length:
                frequencies.append(file.count(self.methods[i]))
                i = i + 1
            self.db_op_target.insert_frequencies(self.columns, frequencies)  # 插入数据
            count = count + 1
            file_name = file_name + 1
        self.db_op_source.finalize()
        self.db_op_target.finalize()

    def get_columns(self):
        columns = []
        for i in range(0, self.methods.__len__()):
            columns.append("'" + self.methods[i] + "'")
        return columns


# class Rename:
#     def __init__(self, dir_path):
#         self.dir_path = dir_path
#
#     def rename(self):
#         i = 1
#         for file in os.listdir(self.dir_path):  # 返回指定的文件夹包含的文件或文件夹的名字的列表
#             if (os.path.isfile(os.path.join(self.dir_path, file)) == True):  # os.path.join进行拼接，os.path.isfile判断是否是文件
#                 new_name = file.replace(file, "%d.js" % i)
#                 os.rename(os.path.join(self.dir_path, file), os.path.join(self.dir_path, new_name))
#                 i += 1
#         print("Good Job. Rename Successfully.")
#
#
# class write_excel():
#     def __init__(self, file_path, list):
#         self.file_path = file_path
#         self.list = list
#
#     def write_excel(self):
#         output = open(self.file_path, 'w', encoding='gbk')
#         output.write('.toSource\t.toString\t.valueOf\n')
#         for i in range(len(self.list)):
#             for j in range(len(self.list[i])):
#                 output.write(str(self.list[i][j]))
#                 output.write('\t')
#             output.write('\n')
#         output.close()
