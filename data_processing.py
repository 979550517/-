#!/usr/bin/env python
# -*- coding: utf-8 -*-import argparse
import logging
import gzip
import sys
import re
import argparse

__version__ = "2.1.1"
__author__ = "刘品博"
__email__ = "979550517@qq.com"

import time


def log_configuration_console():
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s"
    )


def main():
    #
    start = time.time()
    log_configuration_console()
    parser = argparse.ArgumentParser(description=f'\
版本号：{__version__}\
联系方式：{__email__} —— {__author__}',
    usage= '脚本名称 [-h] {子命令}', formatter_class=argparse.RawDescriptionHelpFormatter, prog='PROG')
    subparsers = parser.add_subparsers(help='子命令帮助')

    parser_fq2fa = subparsers.add_parser('fq2fa', help='将fastq文件转化为fasta压缩文件')
    parser_fq2fa.add_argument('file_name', help='输入文件名称',metavar='<FILE>')
    parser_fq2fa.set_defaults(func=fq2fa)

    parser_reads_information = subparsers.add_parser('information', help='查看基因组基本信息（碱基数，N50等）')
    parser_reads_information.add_argument('file_name', help='输入文件名称',metavar='<FILE>')
    parser_reads_information.add_argument('out_file_name', help='输出文件名称', metavar='<OUT_FILE>')
    parser_reads_information.set_defaults(func=reads_information)

    parser_reads_complementary_etc = subparsers.add_parser('complementary_etc', help='输出指定序列互补，反向，反向互补序列')
    parser_reads_complementary_etc.add_argument('file_name', help='输入文件名称',metavar='<FILE>')
    parser_reads_complementary_etc.add_argument('out_file_name', help='输出文件名称', metavar='<OUT_FILE>')
    parser_reads_complementary_etc.add_argument('--Screening_sequence', '-ss', help='输入需要查询的序列ID', default=None,
                                                dest='ss', type=str,metavar=str)
    parser_reads_complementary_etc.add_argument('--start', '-s', help='输入起始位置', default=1, dest='s', type=int,metavar=int)
    parser_reads_complementary_etc.add_argument('--end', '-e', help='输入终止位置', default=-1, dest='e', type=int,metavar=int)
    parser_reads_complementary_etc.set_defaults(func=reads_complementary_etc)

    parser_replace_n = subparsers.add_parser('replace_n', help='将指定序列指定位置替换为N')
    parser_replace_n.add_argument('file_name', help='输入文件名称',metavar='<FILE>')
    parser_replace_n.add_argument('out_file_name', help='输出文件名称', metavar='<OUT_FILE>')
    parser_replace_n.add_argument('--Screening_sequence', '-ss', help='输入需要查询的序列ID', default=None, dest='se', type=str,metavar=str)
    parser_replace_n.add_argument('--start', '-s', help='输入起始位置', default=1, dest='s', type=int,metavar=int)
    parser_replace_n.add_argument('--end', '-e', help='输入终止位置', default=-1, dest='e', type=int,metavar=int)
    parser_replace_n.set_defaults(func=Replace_N)

    args = parser.parse_args()
    args.func(args)
    end = time.time()
    logging.info('程序运行所用时长：%.2f' % (end - start))


def judge_fa_or_fq(x):
    #   x文件名
    if x.endswith('.gz'):
        f = gzip.open(x)
    else:
        f = open(x)
    for line in f:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        if not line:
            continue
        if line.startswith('>'):
            a = True
        else:
            a = False
        break

    return a


def N50(x, y):
    #   reads碱基数列表;y碱基总数
    d = 0
    x.sort()
    for base in x:
        d += base
        if d >= 0.5 * y:
            N50 = base
            break

    return N50


def read_fq(x):
    ## x为文件名
    logging.info('正在读取fastq文件')

    nameseq = []
    if x.endswith('.gz'):
        fq = gzip.open(x)
    else:
        fq = open(x)
    for eachline in fq:
        if isinstance(eachline, bytes):
            eachline = eachline.decode('utf-8')
        eachline = eachline.strip()
        if not eachline:
            continue
        if not nameseq:
            nameseq.append(eachline)
            continue
        nameseq.append(eachline)
        if len(nameseq) == 4:
            yield nameseq
            nameseq = []
    fq.close()

    logging.info('fastq文件读取完毕')


def read_fa(x):
    #   x文件名
    logging.info('正在读取fasta文件')

    temp = ''
    name_seq = []
    if x.endswith('.gz'):
        fa = gzip.open(x)
    else:
        fa = open(x)
    for eachline in fa:
        if isinstance(eachline, bytes):
            eachline = eachline.decode('utf-8')
        eachline = eachline.strip()
        if not eachline:
            continue
        if not name_seq:
            name_seq.append(eachline)
            continue
        if not temp:
            temp = eachline
            continue
        if eachline.startswith('>'):
            name_seq.append(temp)
            temp = ''
        else:
            temp = temp + eachline
            continue
        if len(name_seq) == 2:
            name_seq.extend([None, None])
            yield name_seq
            name_seq = [eachline]
    if not temp:
        pass
    else:
        name_seq.extend([temp, None, None])
        yield name_seq
    fa.close()

    logging.info('fasta文件读取完毕')


def fq2fa(x):
    logging.info('fastq文件正在转换为fasta文件')
    filename = x.file_name
    wt = gzip.open('%s_new.fa.gz' % filename.split(sep='.')[0], 'wb')
    for name, seq, name2, value in read_fq(filename):
        seq.upper
        name = '>' + name[1:]
        name = name.split(sep=' ')[0]
        name_seq = f'{name}\n{seq}\n'
        name_seq = name_seq.encode('ascii')
        wt.write(name_seq)
    wt.close()

    logging.info('fastq文件转换为fasta文件完成')


def reads_information(x):
    logging.info('正在读取数据信息')

    total = []
    total_base = 0
    read = 0
    G = 0
    C = 0
    N = 0
    filename = x.file_name
    if judge_fa_or_fq(filename):
        a = read_fa(filename)
    else:
        a = read_fq(filename)
    for name, seq, none1, none2 in a:
        seq.upper
        seq.strip()
        total.append(len(seq))
        total_base = total_base + len(seq)
        read += 1
        G = G + seq.count('G')
        C = C + seq.count('C')
        N = N + seq.count('N')
        total.sort()
        L_reads = total[-1]
    wt = open(x.out_file_name, 'w')
    content = f'碱基总数：\t{total_base}\nreads总数：\t{read}\t\nreads平均长度：\t{total_base / read:.2f}\nreads最长长度：\t{L_reads}\nN50：\t{N50(total, total_base)}\nGC含量：\t{(G + C) / total_base:.2f}\nN含量：\t{N / total_base:.2f}'
    wt.write(content)
    wt.close()

    logging.info('数据信息读取完毕')


def complementary(x):
    #   x:互补的序列
    x.replace('A', 'L')
    x.replace('T', 'A')
    x.replace('L', 'T')
    x.replace('C', 'K')
    x.replace('G', 'C')
    x.replace('K', 'G')

    return x


def reads_complementary_etc(x):
    logging.info('正在读取reads互补等链')

    line = ''
    filename = x.file_name
    if judge_fa_or_fq(filename):
        a = read_fa(filename)
    else:
        a = read_fq(filename)
    wt = open(x.out_file_name, 'w')
    for name, seq, none1, none2 in a:
        seq.upper #x>X
        if re.match(f'.*{x.ss}.*', name):
            line = seq[x.s:x.e + 1]
        else:
            continue
        name = name.split(sep=' ')[0]
        content = f'序列id:\t{name}\n原始序列：\t{line}\n反向序列：\t{line[::-1]}\n互补序列：\t{complementary(line)}\n反向互补序列：\t{complementary(line[::-1])}'
        wt.write(content)
    if not line:
        logging.error('无匹配序列')
    wt.close()

    logging.info('读取reads互补等链完毕')


def Replace_N(x):
    logging.info('正在替换指定序列')

    filename = x.file_name
    if judge_fa_or_fq(filename):
        a = read_fa(filename)
    else:
        a = read_fq(filename)
    wt = open(x.out_file_name, 'w')
    for name, seq, none1, none2 in a:
        seq.upper
        if re.match(f'.*{x.se}.*', name):
            line = seq[0:x.s] + 'N' * len(seq[x.s:x.e + 1]) + seq[x.e + 1:]
        else:
            line = seq
        if not line:
            logging.error('无匹配序列')
        if none1 == None and none2 == None:
            content = f'{name}\n{line}\n'
        elif none2 != None and none2 != None:
            content = f'{name}\n{line}\n{none1}\n{none2}\n'
        else:
            raise Exception(f'{filename}文件内容格式不正确:\n\t{name}')
        wt.write(content)
    wt.close()

    logging.info('替换指定序列完毕')


if __name__ == '__main__':
    main()
