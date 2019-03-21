class TypeDeductor:
    def __init__(self):
        self.array_characters = [".length", ".concat", ".join", ".pop", ".push",
                                 ".reverse", ".shift", ".slice", ".sort", ".splice", ".toSource",
                                 ".toLocaleString", ".unshift", "[", " ["]
        self.boolean_characters = [".toSource", "!", "! ", "! ", "&&", " &&", "&& ", "||", " ||", "|| ", "^", "=true",
                                   " =true", "= true", " = true", "true=", "true= ", "true =", "true = ", "=false",
                                   " =false", "= false", " = false", "false=", "false= ", "false =", "false = "]
        self.number_characters = [".toLocaleString", ".toFixed", ".toExponential", ".toPrecision", "-=", " -=", "*=",
                                  " *=", "/=", " /=", "++", " ++", "++ ", "--", " --", "-- ", "%", " %", "% "]
        self.string_characters = [".length", ".anchor", ".big", ".blink", ".bold",
                                  ".charAt", ".charCodeAt", ".concat", ".fixed", ".fontsize", ".indexOf", ".italics",
                                  ".lastIndexOf", ".link", ".localeCompare", ".match", ".replace", ".search", ".slice",
                                  ".small", ".split", ".strike", ".sub", ".substr", ".substring", ".sup",
                                  ".toLocaleLowerCase", ".toLocaleUpperCase", ".toLowerCase", ".toUpperCase",
                                  ".toSource", "[", " ["]

    def execute(self, callable):
        params = self.extract_params(callable)
        result = []
        for i in range(0, params.__len__()):
            result.append(self.deduct_param_type(callable, params[i]))
        return result

    def deduct_param_type(self, callable, param_name):
        characters = [self.array_characters, self.boolean_characters, self.number_characters, self.string_characters]
        counter = [0, 0, 0, 0]
        types = ["array", "boolean", "number", "string"]
        for i in range(0, characters.__len__()):
            for j in range(0, characters[i].__len__()):
                target = param_name + characters[i][j]
                if callable.__contains__(target):
                    counter[i] += 1

                target = characters[i][j] + param_name
                if callable.__contains__(target):
                    counter[i] += 1

        max = 0
        for i in range(0, counter.__len__()):
            if counter[i] > max:
                max = counter[i]

        if max > 0:
            result = []
            for i in range(0, counter.__len__()):
                if counter[i] == max:
                    result.append(types[i])
            return result
        else:
            return ['none']

    def extract_params(self, callable):
        left_index = callable.find('(')
        right_index = callable.find(')')
        raw = callable[left_index + 1:right_index]
        if raw.__len__() < 1:
            return []

        params = raw.strip(' ').split(',')
        for i in range(0, params.__len__()):
            params[i] = params[i].strip(' ')
        return params
