
import threading

import similar
from remover import remover


class myThread (threading.Thread):
    def __init__(self, threadID, name, vector,tokens):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delfile = set()
        self.clone = []
        self.vector = vector
        self.tokens = tokens

    def run(self):
        print("start：" + self.name)
        getsimilarity(self)
        print("end" + self.name)

    def getresult(self):
        try:
            return self.vector,self.tokens
        except Exception:
            return None



def getsimilarity (self):

        # print("thread start： " + self.name)

        print("similarity： " + self.name)
        results = []
        for j in range(len(self.vector)):
            resultline = []
            for i in range(len(self.vector)):
                if i > j:
                    break
                else:
                    # 用append
                    result = float('%.03f'%similar.cosine_similarity(self.vector[j], self.vector[i]))
                    resultline.append(result)
                    if result > 0.8:
                        self.delfile.add(j)
                        self.clone.append((i,j))
                    # print("(" + str(j) + "," + str(i) + ")")
            results.append(resultline)

        print("delfile-" + self.name + " :"+ len(self.delfile))

        print("remove clone： " + self.name)

        self.vector = remover(self.name,self.vector,self.clone,self.delfile,self.tokens)

        print("output result " + self.name)

        outputsimilarity = "./output/" + self.name + "similarity.txt"
        with open(outputsimilarity, "w", encoding="UTF-8")as outputencodefile:
            for result in results:
                outputencodefile.write(str(result))
                outputencodefile.write("\n")

        # print("thread end： " + self.name)

