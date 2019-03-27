import os

import creatdict
import similar
from myThread import myThread


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

        if len(vector) < 15:
            vectors1.append(vector)
            token1.append(tokenfile[i])
        elif len(vector) < 25:
            vectors2.append(vector)
            token2.append(tokenfile[i])
        elif len(vector) < 35:
            vectors3.append(vector)
            token3.append(tokenfile[i])
        elif len(vector) < 45:
            vectors4.append(vector)
            token4.append(tokenfile[i])
        elif len(vector) < 60:
            vectors5.append(vector)
            token5.append(tokenfile[i])
        elif len(vector) < 80:
            vectors6.append(vector)
            token6.append(tokenfile[i])
        elif len(vector) < 100:
            vectors7.append(vector)
            token7.append(tokenfile[i])
        elif len(vector) < 150:
            vectors8.append(vector)
            token8.append(tokenfile[i])
        elif len(vector) < 300:
            vectors9.append(vector)
            token9.append(tokenfile[i])
        else:
            vectors10.append(vector)
            token10.append(tokenfile[i])

    #
    # print(len(vectors1))
    # print(len(vectors2))
    # print(len(vectors3))
    # print(len(vectors4))
    # print(len(vectors5))
    # print(len(vectors6))
    # print(len(vectors7))
    # print(len(vectors8))
    # print(len(vectors9))
    # print(len(vectors10))

    threads = []
    wholevector = []
    wholetoken = []

    thread1 = myThread(1, '0-15',vectors1,token1)
    thread2 = myThread(2, '15-25',vectors2,token2)
    thread3 = myThread(3, '25-35',vectors3,token3)
    thread4 = myThread(4, '35-45',vectors4,token4)
    thread5 = myThread(5, '45-60',vectors5,token5)
    thread6 = myThread(6, '60-80',vectors6,token6)
    thread7 = myThread(7, '80-100',vectors7,token7)
    thread8 = myThread(8, '100-150',vectors8,token8)
    thread9 = myThread(9, '150-300',vectors9,token9)
    thread10 = myThread(10, '300+',vectors10,token10)

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

    wholethread = myThread(11, 'whole', wholevector)
    wholethread.start()
    wholethread.join()

    retvec, rettok = wholethread.getresult()

    ####此处返回去重后数据，如何输出到数据库文件


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

