def dianyan(infile, outfile):
    infopen = open(infile,'r', encoding='utf-8')
    outopen = open(outfile,'w', encoding='utf-8')
    lines = infopen.readlines()
    list_1 = []
    for line in lines:
        if line not in list_1:
            list_1.append(line)
            outopen.write(line)
    infopen.close()
    outopen.close()

if __name__ == '__main__':
    dianyan('E:\py\dianyan\dianyan.txt','E:\py\dianyan\dianyan3.txt')
    #dianyan('文本原路径','目标路径')