from wordfreq import WordFreq

methods = [".anchor",".big",".blink",".bold",".charAt",".charCodeAt",".fixed",".fontcolor",".fontsize",".indexOf",".italics",".lastIndexOf",".link",
           ".localeCompare",".match",".replace",".search",".small",".split",".strike",".sub",".substr",".substring",".sup",".toLocaleLowerCase",
            ".toLocaleUpperCase", ".toLowerCase", ".toUpperCase"]  # 2
db_path_source = "../../BrowserFuzzingData/db/js_corpus_final_top_1000.db"  # 文件路径
db_path_target = "../../BrowserFuzzingData/db/result.db"  # 生成文件路径

# 重命名文件
# new_dir = Rename(file_path)
# new_dir.rename()

# 统计方法个数
Array_type = WordFreq(methods, db_path_source, db_path_target)
Array_type.frequence()

# 写入excel
# excel = write_excel(file_path2,list)
# excel.write_excel()
