import re
import gzip
import argparse
import logging
import sys

__version__ = "1.0.1"
__author__ = ("刘品博")
__email__ = "979550517@qq.com"


def log_configuration_console():
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s"
    )


def selected_line(x, y, z):
# x:序列 ; y:起始位置 ; z:终止位置
    t = y - 1
    r = z
    a = x[t:r]

    return a


def read_parameter():
#
    parser = argparse.ArgumentParser(description=f'''
功能：
    提取指定序列的指定区域，并对齐互补，反向以及反向互补

版本号：{__version__}
联系方式：{__email__}——{__author__}
    ''',usage='脚本名称 <文件名称>　【-ss 指定序列】　【-s 起始位置】　【-e 终止位置】',formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('file_name', help='输入文件名称')
    parser.add_argument('--Screening_sequence', '-ss', help='输入需要查询的序列ID', default=None, dest='se', type=str)
    parser.add_argument('--start', '-s', help='输入起始位置', default=1, dest='s', type=int)
    parser.add_argument('--end', '-e', help='输入终止位置', default=-1, dest='e', type=int)
    args = parser.parse_args()

    return args


def replace_specified_location_as_N(a, b, c):
#   a:序列　;　b:起始位点　；　c:终止位点
    e = b - 1
    d = c - 1
    a_1 = a[0:e]
    a_2 = a[d:]
    a = a_1 + 'N' * (c-b) + a_2

    return a


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

    return a


def fq_out(x, z, y):
#   x:序列　; z:指定序列　;　y:文本信息参数
    if isinstance(x, bytes):
        x = x.decode('utf-8')
    x=x.strip()
    if y == 1:
        if len(selected_line(x, read_parameter().s, read_parameter().e)) + 1 == len(x):
            pass
        else:
            x = replace_specified_location_as_N(x, read_parameter().s, read_parameter().e)
        gs.write(f'{x}\n')
        y = 0
    else:
        if re.match(z, x) != None:
            y = 1
        else:
            y = 0
        gs.write(f'{x}\n')

    return y


def fa_element_1(x,z,y,line):
#   x:序列 ; z:指定序列 ; y:文本信息参数 ; line:返回列表（返回序列，文本信息参数）
    if y == 1:
        line = str(x)
        y = 2
    elif y == 0:
        if re.match(z, x) != None:
            y = 1
        else:
            y = 0
        gs.write(f'{x}\n')
    elif y == 2:
        if re.match('^>[a-zA-Z0-9].*', x) != None:
            if len(selected_line(line, read_parameter().s, read_parameter().e)) + 1 == len(
                    line):
                pass
            else:
                line = replace_specified_location_as_N(line, read_parameter().s, read_parameter().e)
            gs.write(f'{line}\n')
            line = ''
            if re.match(z, x) != None:
                y = 1
            else:
                y = 0
            gs.write(f'{x}\n')
        else:
            line = line+x
    a = [line,y]
    return a


def fa_element_2(x,y):
#
    if y == 0:
        pass
    elif y == 2:
        if len(selected_line(x, read_parameter().s, read_parameter().e)) + 1 == len(x):
            pass
        else:
            x = replace_specified_location_as_N(x, read_parameter().s, read_parameter().e)
        gs.write(f'{x}\n')



def fa_out(x, z,y=0):
#
    line = ''
    if x.endswith(".gz"):
        er = gzip.open(x)
    else:
        er = open(x)
    for eachline in er:
        if isinstance(eachline, bytes):
            eachline = eachline.decode('utf-8')
        eachline = eachline.strip()
        fa = fa_element_1(eachline, z, y, line)
        y = fa[1]
        line = fa[0]
    fa_element_2(line, y)


def main():
    #
    if read_parameter().file_name.endswith(".gz"):
        if determine_file_format(read_parameter().file_name):
            for eachline in gzip.open(read_parameter().file_name):
                y = fq_out(eachline, new_a, y)
            logging.info('压缩文件，fastq格式')
        else:
            fa_out(read_parameter().file_name, new_a)
            logging.info('压缩文件，fasta格式')
    else:
        if determine_file_format(read_parameter().file_name):
            for eachline in open(read_parameter().file_name):
                y = fq_out(eachline, new_a, y)
            logging.info('普通文件，fastq格式')
        else:
            fa_out(read_parameter().file_name, new_a)
            logging.info('普通文件，fasta格式')


if __name__ == '__main__':
    y = 0
    new_a = '.*' + read_parameter().se.strip('\'') + '.*'
    log_configuration_console()
    gs = open(f'new_{read_parameter().file_name}.txt', 'w')
    main()
    gs.close()