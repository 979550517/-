import re
import gzip
import argparse
import logging
import sys
import xlwt

__version__ = "1.0.0"
__author__ = ("刘品博")
__email__ = "979550517@qq.com"


def read_parameter():
#
    parser = argparse.ArgumentParser(description=f'''
功能：
    输出文件格式类型，碱基数量,reads总数,N50，reads平均长度,reads最长长度和GC含量（支持压缩文件格式和非压缩文件）

版本号：{__version__}
联系方式：{__email__}————{__author__}
    ''',usage='脚本名称 <文件名称>',formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('file_name', help='输入文件名称')
    args = parser.parse_args()

    return args


def log_configuration_console():
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s"
    )


def determine_file_format(x):
#   x:文件名
    if x.endswith(".gz"):
        we = gzip.open(x)
    else:
        we = open(x)
    for i in we:
        if isinstance(i, bytes):
            i = i.decode('utf-8')
        i = i.strip()
        if re.match('^@', i) != None:
            a = True
        else:
            a = False
        break
    we.close()
    return a


def read_fq(x):
#   x:文件名
    logging.info(f'正在读取fastq文件{x}')
    seq1 = []
    if read_parameter().file_name.endswith(".gz"):
        fq_open = gzip.open(read_parameter().file_name)
    else:
        fq_open = open(read_parameter().file_name)
    for line in fq_open:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()
        if not line:
            continue
        if not seq1:
            seq1.append(line)
            continue
        seq1.append(line)
        if len(seq1) == 4:
            yield seq1
            seq1 = []
    fq_open.close()
    logging.info('文件读取完成')

def out(x):
#   迭代数集
    total = []
    read = 0
    G = []
    C = []
    N = []
    c = []
    g = []
    n = []
    for name,seq,num3,quality in x:
        seq.strip()
        total.append(len(seq))
        read += 1
        G.append(seq.count('G'))
        C.append(seq.count('C'))
        g.append(seq.count('g'))
        c.append(seq.count('c'))
        N.append(seq.count('N'))
        n.append(seq.count('n'))
    ret = {'每行碱基数':total,'reads数':read,'每行G':G,'每行C':C,'每行N':N,'每行g':g,'每行c':c,'每行n':n}
    return ret

def base_total(total):
#
    base_total = 0
    for base in total:
        base_total += base

    return base_total

def reads＿quantity(read):
    reads_quantity = read

    return reads_quantity

def N50_out(total):
    d = 0
    total.sort()
    for base2 in total:
        d += base2
        if d >= 0.5*base_total(total):
            N50_out = base2
            break

    return N50_out

def longest_reads(total):
    total.sort()
    longest_reads = total[-1]

    return longest_reads

def GC_percentage(G,C,c,g,total):
    Gq=0
    Cq=0
    cq=0
    gq=0
    for l in G:
        Gq += l
    for m in C:
        Cq += m
    for n in c:
        cq += n
    for zx in g:
        gq += zx
    GC = (Gq + Cq + cq + gq) / base_total(total)
    GC = round(GC,2)

    return GC

def  N_percentage(N,n,total):
    Nq = 0
    nq = 0
    for i in N:
        Nq += i
    for q in n:
        nq += q
    N = (Nq+nq)/base_total(total)
    N = round(N,2)

    return N


def read_fa(x):
#   x:文件名
    logging.info(f'正在读取fasta文件{x}')
    seq1 = []
    temp = ''
    if read_parameter().file_name.endswith(".gz"):
        fa_open = gzip.open(read_parameter().file_name)
    else:
        fa_open = open(read_parameter().file_name)
    for line in fa_open:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()
        if not line:
            continue
        if not seq1:
            seq1.append(line)
            continue
        if not temp:
            temp = line
            continue
        else:
            if re.match('^>',line):
                seq1.append(temp)
                temp = ''
            else:
                temp = temp+line
                continue
            if len(seq1) == 2:
                seq1.append(None)
                seq1.append(None)
                yield seq1
                seq1 = [line]
    fa_open.close()
    logging.info('文件读取完成')

def configure_CSV(a):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    worksheet.write(0,0,label = '碱基总数')
    worksheet.write(1, 0, label='reads总数')
    worksheet.write(2, 0, label='N50')
    worksheet.write(3, 0, label='reads平均长度')
    worksheet.write(4, 0, label='reads最长长度')
    worksheet.write(5, 0, label='GC含量')
    worksheet.write(6, 0, label='N含量')
    logging.info('正在计算碱基总数')
    worksheet.write(0,1,base_total(a['每行碱基数']))
    logging.info('碱基总数计算完毕')

    logging.info('正在计算reads总数')
    worksheet.write(1,1,reads＿quantity(a['reads数']))
    logging.info('reads总数计算完毕')

    logging.info('正咋计算N50')
    worksheet.write(2,1,N50_out(a['每行碱基数']))
    logging.info('N50计算完毕')

    logging.info('正在计算reads平均长度')
    worksheet.write(3,1,base_total(a['每行碱基数'])/reads＿quantity(a['reads数']))
    logging.info('reads平均长度计算完毕')

    logging.info('正在计算最长read长度')
    worksheet.write(4,1,longest_reads(a['每行碱基数']))
    logging.info('最长read长度计算完毕')

    logging.info('正在计算GC含量')
    worksheet.write(5,1,GC_percentage(a['每行G'],a['每行C'],a['每行c'],a['每行g'],a['每行碱基数']))
    logging.info('GC含量计算完毕')

    logging.info('正在计算N含量')
    worksheet.write(6,1,N_percentage(a['每行N'], a['每行n'], a['每行碱基数']))
    logging.info('N含量计算完毕')

    workbook.save('essential_information.xls')



def main():
    log_configuration_console()
    read_parameter()
    if determine_file_format(read_parameter().file_name):
        a = out(read_fq(read_parameter().file_name))
    else:
        a = out(read_fa(read_parameter().file_name))
    configure_CSV(a)

if __name__ =="__main__":
    main()

