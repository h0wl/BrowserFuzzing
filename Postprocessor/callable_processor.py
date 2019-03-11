# coding:utf-8
import random
import re

from six import unichr


class CallableProcessor:
    def __init__(self, callables):
        self.functions = [self.generate_integer, self.generate_float_point, self.generate_string, self.generate_boolean,
                          self.generate_null, self.generate_undefined, self.generate_array_of_different_type,
                          self.generate_array_of_same_type, self.generate_function]
        self.callables = callables

    def generate_integer(self):
        return str(random.randint(-9007199254740992, 9007199254740992))

    def generate_float_point(self):
        return str(self.generate_integer()) + (str(random.random())[1:])

    def generate_string(self):
        length = random.randint(1, 1024)
        result = ''
        start, end = (0, 55296)
        while length > 0:
            try:
                result += unichr(random.randint(start, end))
            except UnicodeEncodeError:
                pass
            length -= 1
        result.replace('"', '\"')
        result.replace("'", "\'")
        result.replace('\n', '')
        result.replace('\r', '')
        return '"' + result + '"'

    def generate_boolean(self):
        return str(bool(random.randint(0, 1))).lower()

    def generate_null(self):
        return 'null'

    def generate_undefined(self):
        return 'undefined'

    def generate_array_of_different_type(self):
        length = random.randint(0, 9)
        result = '[' + self.generate_a_random_typed_param()
        while length > 0:
            result += (', ' + self.generate_a_random_typed_param())
            length -= 1
        result += ']'
        return result

    def generate_array_of_same_type(self):
        length = random.randint(0, 15)
        choice = random.randint(0, self.functions.__len__() - 1)
        # 如果选中了数组作为元素的类型，更换类型以避免无限递归
        while self.functions[choice] == self.generate_array_of_same_type or self.functions[
            choice] == self.generate_array_of_different_type:
            choice = random.randint(0, self.functions.__len__() - 1)
        result = '[' + self.functions[choice]()
        while length > 0:
            result += (', ' + self.functions[choice]())
            length -= 1
        result += ']'
        return result

    def generate_a_random_typed_param(self):
        choice = random.randint(0, self.functions.__len__() - 1)
        return self.functions[choice]()

    def generate_function(self):
        index = random.randint(0, self.callables.__len__() - 1)
        param_function = self.callables[index].__getitem__(0).decode()
        return re.sub('function[\s\S]*?\(', 'function(', param_function).rstrip(';')

    def extract_function_name(self, function_body: str):
        index_of_function = function_body.find('function', 0)
        index_of_open_parenthesis = function_body.find('(', index_of_function)
        function_name = function_body[index_of_function + 8:index_of_open_parenthesis]
        return function_name.strip()

    def extract_num_of_params(self, function_body: str):
        index_of_open_parenthesis = function_body.find('(', 0)
        index_of_close_parenthesis = function_body.find(')', index_of_open_parenthesis + 1)
        params = function_body[index_of_open_parenthesis + 1:index_of_close_parenthesis]
        params = params.replace(' ', '')
        if params.__eq__(''):
            return 0
        return params.split(',').__len__()

    def generate_self_calling(self, function_body: str):
        function_name = self.extract_function_name(function_body)
        num_of_param = self.extract_num_of_params(function_body)
        self_calling = '('
        if num_of_param > 0:
            self_calling += self.functions[random.randint(0, self.functions.__len__() - 1)]()
            num_of_param -= 1
        while num_of_param > 0:
            self_calling += ', '
            self_calling += self.functions[random.randint(0, self.functions.__len__() - 1)]()
            num_of_param -= 1
        self_calling += ')'

        if function_name.__eq__(''):
            function_body = 'var a = ' + function_body
            result = function_body + '\n' + 'a' + self_calling + ';'
            return result
        else:
            result = function_body + '\n' + function_name + self_calling + ';'
            return result

    def get_random_self_calling(self):
        choice = random.randint(0, self.callables.__len__() - 1)
        function_body = self.callables[choice].__getitem__(0).decode()
        return self.generate_self_calling(function_body)

    def get_self_calling(self, function_body):
        return self.generate_self_calling(function_body)
