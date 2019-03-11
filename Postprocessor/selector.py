import os
import re
import subprocess

from db_operation import DBOperation
from callable_processor import CallableProcessor


class Selector:
    def __init__(self, db_path, save_path, target_count=100, temper_round=100):
        self.db_op = DBOperation(db_path, 'corpus')
        self.callables = self.db_op.query_all()
        self.callable_processor = CallableProcessor(self.callables)
        self.save_path = save_path
        self.target = target_count
        self.temper_round = temper_round

    def execute(self):
        index_of_callables = 0
        i = 0
        while i < self.target:
            try:
                function_body = self.callables[index_of_callables].__getitem__(0).decode('utf-8')
                test_case = ''
                self_calling = self.callable_processor.get_self_calling(function_body)
                self.create_and_fill_file('./ISTANBUL_TEST_CASE.js', self_calling)
                st, br, fu, li = self.istanbul_cover('ISTANBUL_TEST_CASE.js')

                for j in range(0, self.temper_round):
                    self_calling = self.callable_processor.get_self_calling(function_body)
                    self.create_and_fill_file('./ISTANBUL_TEST_CASE.js', self_calling)
                    st_tmp, br_tmp, fu_tmp, li_tmp = self.istanbul_cover('ISTANBUL_TEST_CASE.js')
                    if st_tmp - st + br_tmp - br + fu_tmp - fu + li_tmp - li > 0:
                        test_case.join('')  # 必要！这一句为了扩展一下test_case变量的作用域
                        test_case = self_calling
                        st, br, fu, li = self.set_coverage_values(st_tmp, br_tmp, fu_tmp, li_tmp)
                    os.remove('./ISTANBUL_TEST_CASE.js')
                if test_case.__len__() > 0:
                    self.create_and_fill_file(self.save_path + '/' + str(i) + '.js', test_case)
                    i += 1
                index_of_callables += 1
            except Exception:
                pass

    def create_and_fill_file(self, file_path, content):
        with open(file_path, 'a') as file:
            file.write(content)

    def set_coverage_values(self, st_tmp, br_tmp, fu_tmp, li_tmp):
        return st_tmp, br_tmp, fu_tmp, li_tmp

    def istanbul_cover(self, file_name):
        st, br, fu, li = self.set_coverage_values(0, 0, 0, 0)

        cmd = ['istanbul', 'cover', file_name]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.poll()
        stdout_list = p.stdout.readlines()
        stdout = ''
        for line in stdout_list:
            stdout = stdout + line.decode('utf-8')
        coverage_of_single_sample = re.findall(': [\s\S]*?%', stdout)
        if coverage_of_single_sample.__len__() == 4:
            st = re.sub('%', '', re.sub(': ', '', coverage_of_single_sample[0]))
            br = re.sub('%', '', re.sub(': ', '', coverage_of_single_sample[1]))
            fu = re.sub('%', '', re.sub(': ', '', coverage_of_single_sample[2]))
            li = re.sub('%', '', re.sub(': ', '', coverage_of_single_sample[3]))
        return float(st), float(br), float(fu), float(li)


if __name__ == '__main__':
    db_path = '../../BrowserFuzzingData/db/js_corpus_final.db'
    save_path = '../../BrowserFuzzingData/selected'
    selector = Selector(db_path, save_path, temper_round=100)
    selector.execute()
