
import creatdict
import similar

def find(token,dict):
    # try:
    for tokens in dict:
        if tokens[0] == token:
            #要把token[1]转成int类型
            return int(tokens[1])
        else:
            return -1



def encode(tokens,dict):
    flag = -1
    afterencode = []
    for token in tokens:
        for dicttoken in dict:
            if token == dicttoken[0]:
                flag = dicttoken[1]
                break
        afterencode.append(flag)
        flag = -1
    return afterencode

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
    vectors = []
    results = []
    # dbfile = creatdict.readdb()

    print("Encode")

    for i in range(len(tokenfile)):
        # line = line[0].decode("UTF-8")

        # tokens = creatdict.code2tokens(line)
        vector = encode(tokenfile[i], dict)
        # print(vector)
        vectors.append(vector)

    # with open(".\\output\\jsfile.txt","r",encoding="UTF-8") as filepath:
    #     for line in filepath.readlines():
    #         line = line[:-1]
    #         with open(".\\output\\"+ line,"r",encoding="UTF-8") as codefile:
    #             code = codefile.read()
    #             tokens = creatdict.code2tokens(code)
    #             vector =encode(tokens,dict)
    #             # print(vector)
    #             vectors.append(vector)

    outputencode = "./output/outputencoder.txt"
    with open("./output/outputencoder.txt","w",encoding="UTF-8")as outputencodefile:
        for vector in vectors:
            outputencodefile.write(str(vector))
            outputencodefile.write("\n")

    # vectors = unifinevector(vectors)

    print()
    for j in range(len(vectors)):
        resultline = []
        for i in range(len(vectors)):
            if i > j:
                break;
            else:
            #用append
                resultline.append(similar.cosine_similarity(vectors[j], vectors[i]))
                print("("+ str(j) + "," + str(i) + ")")
        results.append(resultline)

    outputsimiliarity = "./output/outputsimilarity.txt"

    with open("./output/outputsimilarity.txt",'w',encoding="UTF-8") as outputfile:

        for result in results:
            for i in range(len(result)):
                outputfile.write(str(result[i]))
                outputfile.write("\t")
            outputfile.write("\n")

