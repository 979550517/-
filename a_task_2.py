import gzip
import re
import not_gz_fastq_task2
import not_gz_fasta_task2
import gz_fastq_task2
import gz_fasta_task2
import argparse
parser = argparse.ArgumentParser(description="判断文件类型，输出碱基总数，reads总数,N50，reads平均长度,reads最长长度和GC含量，支持压缩文件格式和非压缩文件格式",usage='脚本名称＋文件名称')
parser.add_argument('file_name',help='输入文件名称')
args = parser.parse_args()
data_name = args.file_name
name_split = data_name.split(sep='.')
name_finall = name_split[-1]
if name_finall == 'gz':
    with gzip.open(data_name) as p:
        for o in p:
            new_o = o.decode('utf-8')
            if re.match('^@', new_o) != None:
                a = 1
            else:
                a = 0
            break
        if a == 1:
            #文件类型为fastq
            print('数据文件类型为压缩fastq')
            # 碱基总数
            jianji = gz_fastq_task2.Base_total(data_name)
            print(f'\n碱基总数为: {jianji}\n')
            # read数目
            reads = gz_fastq_task2.reads_total(data_name)
            print(f'reads的总数为: {reads}\n')
            # N50
            N50 = gz_fastq_task2.N50_out(data_name)
            print(f'N50为： {N50}\n')
            # 平均长度
            averger_read = gz_fastq_task2.averge_length_reads(data_name)
            print(f'reads平均长度为： {averger_read}\n')
            # 最大长度
            length_reads = gz_fastq_task2.length_reads(data_name)
            print(f'最长reads为： {length_reads}\n')
            # GC含量
            GC = gz_fastq_task2.GC(data_name)
            print(f"GC含量为： %0.2f" % GC)
        else:
            #文件类型为fasta
            print('数据文件类型为压缩fasta')
            # 碱基总数
            jianji = gz_fasta_task2.Base_total(data_name)
            print(f'\n碱基总数为: {jianji}\n')
            # read数目
            reads = gz_fasta_task2.reads_total(data_name)
            print(f'reads的总数为: {reads}\n')
            # N50
            N50 = gz_fasta_task2.N50_out(data_name)
            print(f'N50为： {N50}\n')
            # 平均长度
            averger_read = gz_fasta_task2.averge_length_reads(data_name)
            print(f'reads平均长度为： {averger_read}\n')
            # 最大长度
            length_reads = gz_fasta_task2.length_reads(data_name)
            print(f'最长reads为： {length_reads}\n')
            # GC含量
            GC = gz_fasta_task2.GC(data_name)
            print(f"GC含量为： %0.2f" % GC)
else:
    with open(data_name) as q:
        for i in q:
            if re.match('^@[a-zA-Z0-9].*', i) != None:
                #判断文件类型为fasta or fastq
                a = 1
            else:
                a = 0
            break
        if a == 1:
            #文件类型为fastq
            print('数据文件类型为未压缩fastq')
            # 碱基总数
            jianji = not_gz_fastq_task2.Base_total(data_name)
            print(f'\n碱基总数为: {jianji}\n')
            # read数目
            reads = not_gz_fastq_task2.reads_total(data_name)
            print(f'reads的总数为: {reads}\n')
            # N50
            N50 = not_gz_fastq_task2.N50_out(data_name)
            print(f'N50为： {N50}\n')
            # 平均长度
            averger_read = not_gz_fastq_task2.averge_length_reads(data_name)
            print(f'reads平均长度为： {averger_read}\n')
            # 最大长度
            length_reads = not_gz_fastq_task2.length_reads(data_name)
            print(f'最长reads为： {length_reads}\n')
            # GC含量
            GC = not_gz_fastq_task2.GC(data_name)
            print(f"GC含量为： %0.2f" % GC)
        else:
            #文件类型为fasta
            print('数据类型为未压缩fasta')
            # 碱基总数
            jianji = not_gz_fasta_task2.Base_total(data_name)
            print(f'\n碱基总数为: {jianji}\n')
            # read数目
            reads = not_gz_fasta_task2.reads_total(data_name)
            print(f'reads的总数为: {reads}\n')
            # N50
            N50 = not_gz_fasta_task2.N50_out(data_name)
            print(f'N50为： {N50}\n')
            # 平均长度
            averger_read = not_gz_fasta_task2.averge_length_reads(data_name)
            print(f'reads平均长度为： {averger_read}\n')
            # 最大长度
            length_reads = not_gz_fasta_task2.length_reads(data_name)
            print(f'最长reads为： {length_reads}\n')
            # GC含量
            GC = not_gz_fasta_task2.GC(data_name)
            print(f"GC含量为： %0.2f" % GC)