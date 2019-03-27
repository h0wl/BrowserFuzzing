

def remover(name,vectors,clone,delfile,tokens):
    outfile = "./output/" + name + "clonepairs.txt"
    with open(outfile, 'a') as f:
                #                  print(name)
        #输出克隆对
        for i,j in clone:

            f.write(tokens[i])
            f.write('\n')
            f.write(tokens[j])
            f.write('\n')
            f.write("-------------------------------------------------------------------------------------------------")

        for d in delfile:
            vectors.pop(d)
            tokens.pop(d)
    return vectors



