import gzip
import re
import argparse
b = 0
c = '\n'
parser = argparse.ArgumentParser(description="将fastq文件转化为fasta文件，仅支持压缩文件格式",usage='脚本名称＋压缩文件名称')
parser.add_argument('file_name',help='输入文件名称')
args = parser.parse_args()
data_name = args.file_name
new_data_name = data_name.split(sep='.')
new_data_name = new_data_name[0]+'.fa.'+new_data_name[-1]
data_zip = gzip.open(data_name, 'r')
for eachline in data_zip:
    data_normal = eachline.decode('utf-8')
    if b == 1:
        data_normal2 = data_normal.encode('ascii')
        with gzip.open("new_%s" % new_data_name, 'ab+') as g:
            g.write(data_normal2)
            b = 0
    else:
        if re.match('^@[a-zA-Z0-9].*',data_normal) != None :
            data_normal = data_normal.replace('@','>',1)
            data_normal2 = data_normal.split()
            data_normal2 = data_normal2[0]
            data_normal2 = data_normal2 + c
            data_normal2 = data_normal2.encode('ascii')
            with gzip.open(f'new_{new_data_name}','ab+') as g:
                g.write(data_normal2)
                b=1
