import re
import gzip
def Base_total(x):
    b=0
    total = []
    d = 0
    data_zip = gzip.open(x)
    for eachline in data_zip:
        data_normal = eachline.decode('utf-8')
        if b == 1:       #判断是否为碱基序列，是直接输出，否继续向下执行判断命令
                total.append(len(data_normal))
                b = 0
        else:
        #逐行判断是否含有＠开头文字
            if re.match('^>',data_normal) != None :
            #是：输出该段二进制文字及下一行二进制文字
                b=1
    data_zip.close()
    for i in total:
        d+=i
    return d

def reads_total(x):
    a = 0
    data_zip = gzip.open(x)
    for eachline in data_zip:
        eachline = eachline.decode('utf-8')
        if re.match('^>', eachline) != None:
            a += 1
    return a

def N50_out(x):
    b = 0
    d = 0
    e = 0
    total = list()
    data_zip = gzip.open(x)
    for eachline in data_zip:
        eachline = eachline.decode('utf-8')
        if b == 1:  # 判断是否为碱基序列，是直接输出，否继续向下执行判断命令
            total.append(len(eachline))
#            qwe = len(eachline)
            b = 0
        else:
            # 逐行判断是否含有＠开头文字
            if re.match('^>', eachline) != None:
                # 是：输出该段二进制文字及下一行二进制文字
                b = 1
    data_zip.close()
    for i in total:
        e+=i
    p = 0.5*e
    total.sort()
    for c in total:
        if d >= p:
            break
        else:
            d += c
    return c

def averge_length_reads(x):
    b=0
    total = []
    d = 0
    e = 0
    data_zip = gzip.open(x)
    for eachline in data_zip:
        eachline = eachline.decode('utf-8')
        if b == 1:       #判断是否为碱基序列，是直接输出，否继续向下执行判断命令
                total.append(len(eachline))
                b = 0
        else:
        #逐行判断是否含有＠开头文字
            if re.match('^>',eachline) != None :
            #是：输出该段二进制文字及下一行二进制文字
                b=1
    data_zip.close()
    for i in total:
        e+=1
        d+=i
    r = d/e
    return r

def length_reads(x):
    b = 0
    d = 0
    e = 0
    total = list()
    data_zip = gzip.open(x)
    for eachline in data_zip:
        eachline = eachline.decode('utf-8')
        if b == 1:  # 判断是否为碱基序列，是直接输出，否继续向下执行判断命令
            total.append(len(eachline))
            #            qwe = len(eachline)
            b = 0
        else:
            # 逐行判断是否含有＠开头文字
            if re.match('^>', eachline) != None:
                # 是：输出该段二进制文字及下一行二进制文字
                b = 1
    data_zip.close()
    total.sort()
    return total[-1]

def GC(x):
    b=0
    total = []
    G=[]
    C = []
    c = []
    g = []
    d = 0
    e = 0
    f = 0
    t = 0
    y = 0
    data_zip = gzip.open(x)
    for eachline in data_zip:
        eachline = eachline.decode('utf-8')
        if b == 1:       #判断是否为碱基序列，是直接输出，否继续向下执行判断命令
                total.append(len(eachline))
                G.append(eachline.count('G'))
                C.append(eachline.count('C'))
                g.append(eachline.count('g'))
                c.append(eachline.count('c'))
                b = 0
        else:
        #逐行判断是否含有＠开头文字
            if re.match('^>',eachline) != None :
            #是：输出该段二进制文字及下一行二进制文字
                b=1
    data_zip.close()
    for i in total:
        d+=i
    for l in G:
        e+=l
    for m in C:
        f+=m
    for n in c:
        t+=n
    for zx in g:
        y+=zx
    qwe = (e+f+t+y)/d
    return qwe