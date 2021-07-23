#!/usr/bin/env python
# -*- coding: utf-8 -*-import argparse
import logging
import gzip
import sys
import argparse
import threading
import time

__version__='1.0.0'

def read_fq(x):
    ## x为文件名
    logging.info('正在读取fastq文件')
    start = time.time()
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
    end = time.time()
    logging.info('fastq文件读取完毕')
    logging.info('文件读取所用时长：%.2f' % (end-start))


def fq2fa(name,seq):

        seq.upper
        name = '>' + name[1:]
        name = name.split(sep=' ')[0]
        name_seq = f'{name}\n{seq}'
        print(name_seq)



def log_configuration_console():
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s"
    )


def cut_yield(args):
    line = 0
    for name,seq,none1,none2 in read_fq(args.file_name):
        if line == 0:
            mythread_1 = threading.Thread(target=fq2fa, args=(name,seq))
            mythread_1.start()
            line +=1
            continue
        elif line == 1:
            mythread_2 = threading.Thread(target=fq2fa, args=(name,seq))
            mythread_2.start()
            line +=1
            continue
        elif line == 2:
            mythread_3 = threading.Thread(target=fq2fa, args=(name,seq))
            mythread_3.start()
            line +=1
            continue
        while True:
            if not mythread_1.is_alive:
                mythread_1 = threading.Thread(target=fq2fa, args=(name,seq))
                mythread_1.start()
                break
            if not mythread_2.is_alive():
                mythread_2 = threading.Thread(target=fq2fa, args=(name,seq))
                mythread_2.start()
                break
            if not mythread_3.is_alive():
                mythread_3 = threading.Thread(target=fq2fa, args=(name,seq))
                mythread_3.start()
                break

    thread = []
    thread.append(mythread_1)
    thread.append(mythread_2)
    thread.append(mythread_3)
    for i in thread:
        i.join()

def main():
    #
    start = time.time()
    log_configuration_console()
    parser = argparse.ArgumentParser(description=f'''
功能：
    fq2fa
    ''', usage='脚本名称 [-h] {子命令}   ', formatter_class=argparse.RawDescriptionHelpFormatter, prog='PROG')
    parser.add_argument('file_name', help='输入文件名称')
    args = parser.parse_args()
    cut_yield(args)

    end = time.time()
    logging.info('程序运行所用时长：%.2f' % (end - start))


if __name__ == '__main__':
    main()