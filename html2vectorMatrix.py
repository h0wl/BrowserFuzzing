#coding:utf8

'''
输入 html文件 输出一个向量矩阵
忽略:
	- 标签间的内容
	- 不规范的标签书写方式
'''

import random
import sys
import re

# 从本地文件读取标签并返回list(这两个键值对相反)
def getTagList():
	tagList = [] # 初始化标签list
	try:
		with open('all_tag','r',encoding="utf8") as file:
			for line in file:
				line = line.replace('\n','').split(' ')
				tagList.append(line[0])
	except:
		print('[!] TagList Read Error !')
		sys.exit(0)
	return tagList
		
# 输入一个本地文件，返回字符串
def readFile(file_path):
	html_string = ''
	pat = '[\r\n\t]'
	try:
		with open(file_path,'r',encoding="utf8") as file:
			html_string = re.compile(pat).sub('',file.read())
	except:
		print('[!] Html Read Error !')
	return html_string
	
# 输入html字符串，返回向量矩阵（二维list）
def generateMatrix(html_str,tagList):
	tag_pat = "<(.*?)>" # 提取正则
	
	vector_matrix = [] # 初始化向量矩阵
	
	html_list = re.compile(tag_pat,re.S).findall(html_str) # 正则匹配标签
	
	l_vector = generateVector("<",tagList)
	r_vector = generateVector(">",tagList)
	
	for str in html_list:
		vector_matrix.append(l_vector) # 存入左标签的向量
		
		vector_matrix+=string2matrix(str,tagList)
		
		vector_matrix.append(r_vector) # 存入右标签的向量
	
	return vector_matrix
		
# 输入一个字符串和标签数组，如果字符串存在标签中
def generateVector(str,tagList):
	if str.lower() in tagList: # 字符串存在于字典中
		vector = [0 for i in range(len(tagList))]
		tag_index = tagList.index(str)
		vector[tag_index] = 1
	else: # 字典中不存在此tag
		vector = str
	return vector
		
# 输入字符串，返回一个对应的向量矩阵
def string2matrix(str,tagList):
	tmp_matrix = []
	list = str.split(' ')
	for i in list:
		if i.lower() in tagList: # 若i在标签字典中存在
			tmp_matrix.append(generateVector(i.lower(),tagList)) # 向矩阵中添加向量
		else: # 若不存在，说明需要进一步切割
			result = deepSplit(i) # 深度切割，获取一个字符串list
			for j in result: # 遍历
				if j.lower() in tagList:
					tmp_matrix.append(generateVector(j.lower(),tagList))
				else: #此词大概率是字典中未出现过的词
					tmp_matrix.append(j)
	return tmp_matrix
		
# 输入字符串(特点:没有空格)，切割返回一个list
def deepSplit(str):
	result = []
	
	pat1 = "^(/)(.*)" # 匹配类似 /body   /p
	
	pat2 = '''(.*?)(=)(["'])(.*?)(["'])'''
	
	# -----------------------------
	
	data_pat = "data(-.*)" # 匹配 data-*
	
	r = re.compile(pat1).findall(str)
	
	if len(r) == 0:
		r = re.compile(pat2).findall(str)
		if len(r) == 0:
			result.append(str)
			
	for tuple in r:
		for i in tuple:
			temp_r = re.compile(data_pat).findall(i)
			if len(temp_r) != 0:
				result.append("data-*")
			else:
				result.append(i)
	return result
	
# 输入一个向量矩阵，将其一串html字符串
def matrix2string(matrix,tagList):
	string = '' # 初始化输出字符串
	for vector in matrix: # 遍历矩阵中的每个向量
		if type(vector).__name__ == 'list':
			tag_index = vector.index(1)
			string+=tagList[tag_index]
		else: # elif type(vector).__name__ == 'str' # 表示是未加入字典中的标签
			string+=vector
		string+=' '
	return string
	
# 分析当前向量矩阵，查看未转换为向量的词有哪些,accuracy表示上下文精度
def analyzeMatrix(matrix,tagList,accuracy=4):
	for i in range(len(matrix)): # matrix[i]代表一个向量
		if type(matrix[i]).__name__ == 'str': # 表示未转成向量
			string = ''
			for j in range(accuracy):
				try: string+=tagList[matrix[i-accuracy+j].index(1)]+' '
				except: pass
			string+=matrix[i]
			for j in range(accuracy):
				try: string+=tagList[matrix[i+j+1].index(1)]+' '
				except: pass
			print('[*] 陌生TAG=>'+matrix[i]+'\t上下文=>'+string)

if __name__ == '__main__':
	tagList = getTagList() # 读取本地字典
	
	html_str = readFile('./index.html') # 读取本地index.html文件
	
	vector_matrix = generateMatrix(html_str,tagList) # 获取向量矩阵
	
	# 打印向量矩阵
	# for i in vector_matrix:
		# print(i)
	
	# html_string = matrix2string(vector_matrix,tagList) # 将矩阵还原成html字符串
	# 打印html字符串
	# print(html_string)
	
	# 分析矩阵
	analyzeMatrix(vector_matrix,tagList)
	
	# print(len(vector_matrix))
	
	# -------------------下面是执行测试----------------
	
	# path = './test_html'
	
	# sum_500 = 0
	# sum_1000 = 0
	# sum_1500 = 0
	# sum_2000 = 0
	
	# count = 0
	# sum = 0
	# for i in os.listdir(path):
		# html_path = path+'/'+i
		# if os.path.isfile(html_path):
			# html_str = readFile(html_path) # 读取本地index.html文件
			# vector_matrix = generateMatrix(html_str,tagList) # 获取向量矩阵
			# count+=1
			# sum+=len(vector_matrix)
			# if len(vector_matrix) < 500:
				# sum_500+=1
			# elif len(vector_matrix) < 1000:
				# sum_1000+=1
			# elif len(vector_matrix) < 1500:
				# sum_1500+=1
			# elif len(vector_matrix) < 2000:
				# sum_2000+=1
	# print(sum_500)
	# print(sum_1000)
	# print(sum_1500)
	# print(sum_2000)