import os

import creatdict
import similar
from myThread import myThread

from db_operation1 import DBOperation


def remove(tokenfile,vector,i,j):
    outfile = "./output/clonepairs.txt"
    with open(outfile, 'a') as f:
                #                  print(name)
        f.write(tokenfile[i])
        f.write('\n')
        f.write(tokenfile[j])
        f.write('\n')
    vector.pop(j)
    return vector

def encode(tokens,dict):
    flag = -1
    afterencode = []
    resulttuple = set()
    for token in tokens:
        # for dicttoken in dict:
        #     if token == dicttoken[0]:
        #         flag = dicttoken[1]
        #         break
        flag = dict.get(token)
        if flag == None:
            flag = -1

        afterencode.append(flag)

    resulttuple = tuple(afterencode)
    afterencode = []
    # print(resulttuple)

    return resulttuple

#补零还是切割呢？

def unifinevector(vectors):
    maxlen = 3000
    # for vector in vectors:
    #     if len(vector) >maxlen:
    #         maxlen = len(vector)

    newvectors = []
    for vector in vectors:
        newvector = list(vector)
        if len(newvector) < maxlen:
            for i in range(maxlen - len(newvector)):
                newvector.append(0)
        else:
            newvector = newvector[:3000]
        newvectors.append(newvector)


    return newvectors



if __name__ == '__main__':



    print("Processing dict\n")
    dict,tokenfile = creatdict.creatdict()

    vectors1 = []
    vectors2 = []
    vectors3 = []
    vectors4 = []
    vectors5 = []
    vectors6 = []
    vectors7 = []
    vectors8 = []
    vectors9 = []
    vectors10 = []
    results = []

    token1 = []
    token2 = []
    token3 = []
    token4 = []
    token5 = []
    token6 = []
    token7 = []
    token8 = []
    token9 = []
    token10 = []

    # dbfile = creatdict.readdb()

    print("Encode")

    for i in range(len(tokenfile)):

        #此处的vector是tuple
        vector = encode(tokenfile[i], dict)

        if len(vector) < 25:
            vectors1.append(vector)
            token1.append(tokenfile[i])
        elif len(vector) < 35:
            vectors2.append(vector)
            token2.append(tokenfile[i])
        elif len(vector) < 45:
            vectors3.append(vector)
            token3.append(tokenfile[i])
        elif len(vector) < 60:
            vectors4.append(vector)
            token4.append(tokenfile[i])
        elif len(vector) < 80:
            vectors5.append(vector)
            token5.append(tokenfile[i])
        elif len(vector) < 120:
            vectors6.append(vector)
            token6.append(tokenfile[i])
        elif len(vector) < 200:
            vectors7.append(vector)
            token7.append(tokenfile[i])
        elif len(vector) < 300:
            vectors8.append(vector)
            token8.append(tokenfile[i])
        elif len(vector) < 500:
            vectors9.append(vector)
            token9.append(tokenfile[i])
        else:
            vectors10.append(vector)
            token10.append(tokenfile[i])


    print(len(vectors1))
    print(len(vectors2))
    print(len(vectors3))
    print(len(vectors4))
    print(len(vectors5))
    print(len(vectors6))
    print(len(vectors7))
    print(len(vectors8))
    print(len(vectors9))
    print(len(vectors10))

    threads = []
    wholevector = []
    wholetoken = []

    thread1 = myThread(1, '0-25',vectors1,token1)
    thread2 = myThread(2, '25-35',vectors2,token2)
    thread3 = myThread(3, '35-45',vectors3,token3)
    thread4 = myThread(4, '45-60',vectors4,token4)
    thread5 = myThread(5, '60-80',vectors5,token5)
    thread6 = myThread(6, '80-120',vectors6,token6)
    thread7 = myThread(7, '120-200',vectors7,token7)
    thread8 = myThread(8, '200-300',vectors8,token8)
    thread9 = myThread(9, '300-500',vectors9,token9)
    thread10 = myThread(10, '500+',vectors10,token10)

    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)
    threads.append(thread5)
    threads.append(thread6)
    threads.append(thread7)
    threads.append(thread8)
    threads.append(thread9)
    threads.append(thread10)

    for thread in threads:  # start threads 此处并不会执行线程，而是将任务分发到每个线程，同步线程。等同步完成后再开始执行start方法
        thread.start()

    for t in threads:
        t.join()
        retvec,rettok = t.getresult()
        wholevector.extend(retvec)
        wholetoken.extend(rettok)

    print("after " + str(len(wholevector)))

    print("whole Thread")
    #清空各线程list
    vectors1 = []
    vectors2 = []
    vectors3 = []
    vectors4 = []
    vectors5 = []
    vectors6 = []
    vectors7 = []
    vectors8 = []
    vectors9 = []
    vectors10 = []
    # results = []

    token1 = []
    token2 = []
    token3 = []
    token4 = []
    token5 = []
    token6 = []
    token7 = []
    token8 = []
    token9 = []
    token10 = []
    for i in range(len(wholevector)):
        if len(wholevector[i]) < 30:
            vectors1.append(wholevector[i])
            token1.append(wholetoken[i])
        elif len(wholevector[i]) < 60:
            vectors2.append(wholevector[i])
            token2.append(wholetoken[i])
        elif len(wholevector[i]) < 100:
            vectors3.append(wholevector[i])
            token3.append(wholetoken[i])
        elif len(wholevector[i]) < 200:
            vectors4.append(wholevector[i])
            token4.append(wholetoken[i])
        elif len(wholevector[i]) < 400:
            vectors5.append(wholevector[i])
            token5.append(wholetoken[i])

    thread11 = myThread(11, '0-30', vectors1, token1)
    thread12 = myThread(12, '30-60', vectors2, token2)
    thread13 = myThread(13, '60-100', vectors3, token3)
    thread14 = myThread(14, '100-200', vectors4, token4)
    thread15 = myThread(15, '200-400', vectors5, token5)
#清空
    threads1 = []
    wholevector = []
    wholetoken = []

    threads1.append(thread1)
    threads1.append(thread2)
    threads1.append(thread3)
    threads1.append(thread4)
    threads1.append(thread5)

    for threadin1 in threads1:  # start threads 此处并不会执行线程，而是将任务分发到每个线程，同步线程。等同步完成后再开始执行start方法
        threadin1.start()

    for t1 in threads1:
        t1.join()
        retvec, rettok = t1.getresult()
        wholevector.extend(retvec)
        wholetoken.extend(rettok)




    ####此处返回去重后数据，如何输出到数据库文件

    db_path = "./output/final.db"
    db_op = DBOperation(db_path, 'corpus')
    db_op.init_db()
    # callables = db_op.query_all(["Content"])
    # print(callables[0][0].decode('utf-8'))
    for function in wholetoken:
        db_op.insert(["Content"], function)

    db_op.finalize()


    ##############




    print("Exiting Main Thread")




    # outputencode = "./output/outputencoder.txt"
    # with open("./output/outputencoder.txt","w",encoding="UTF-8")as outputencodefile:
    #     for vector in vectors1:
    #         outputencodefile.write(str(vector))
    #         outputencodefile.write("\n")

    # vectors = unifinevector(vectors)

    # print()
    # for j in range(len(vectors1)):
    #     resultline = []
    #     for i in range(len(vectors1)):
    #         if i > j:
    #             break
    #         else:
    #         #用append
    #             resultline.append(similar.cosine_similarity(vectors1[j], vectors1[i]))
    #             print("("+ str(j) + "," + str(i) + ")")
    #     results.append(resultline)

    # outputsimiliarity = "./output/outputsimilarity.txt"
    #
    # with open("./output/outputsimilarity.txt",'w',encoding="UTF-8") as outputfile:
    #
    #     for result in results:
    #         for i in range(len(result)):
    #             outputfile.write(str(result[i]))
    #             outputfile.write("\t")
    #         outputfile.write("\n")

