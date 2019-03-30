

def remover(name,vectors,clone,delfile,tokens):
    outfile = "./output/" + name + "clonepairs.txt"
    with open(outfile, 'a',encoding="UTF-8") as f:
                #                  print(name)
        #输出克隆对
        for i,j in clone:

            f.write("1:" + str(tokens[i]))
            f.write('\n')
            f.write("2:" + str(tokens[j]))
            f.write('\n')
            f.write("-------------------------------------------------------------------------------------------------")
            f.write("\n")

        newvector = []
        newtokens = []

        for i in range(len(vectors)):
            if i not in delfile:
                newvector.append(vectors[i])
                newtokens.append(tokens[i])
    return vectors



