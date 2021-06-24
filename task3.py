import gzip
import re
import task3_tools
import argparse
parser = argparse.ArgumentParser(description="提取指定序列的指定区域，并对齐互补，反向以及反向互补",usage='脚本名称＋文件名称')
parser.add_argument('file_name',help='输入文件名称')
args = parser.parse_args()
data_name = args.file_name
b=0
name_split = data_name.split(sep='.')
name_finall = name_split[-1]
print('\n请输入要提取的序列ID\n')
a = input()
new_a = '.*'+a+'.*'
print('\n请输入提取该序列的起始位置信息（起始位置为1）\n')
s = eval(input())
print('\n请输入提取该序列的终止位置信息（不包含终止位置）\n')
d = eval(input())
if name_finall == 'gz':
    with gzip.open(data_name) as q:
        for line in q:
            eachline = line.decode('utf-8')
            if b == 1:
                r = task3_tools.selected_line(eachline, s, d)
                print(f'\n碱基序列为： {r}\n')
                fanx = task3_tools.fanx(r)
                print(f'反向序列为： {fanx}\n')
                print(f'互补序列为： {task3_tools.hub(r)}\n')
                print(f'反向互补序列为： {task3_tools.fanx_hub(r)}\n')
                b = 0
            else:
                if re.match(new_a, eachline) != None:
                    b=1
                    print(f'序列id为： {eachline}')
else:
    with open(data_name) as w:
        for eachline in w:
            if b == 1:
                r = task3_tools.selected_line(eachline, s, d)
                print(f'\n碱基序列为： {r}\n')
                fanx = task3_tools.fanx(r)
                print(f'反向序列为： {fanx}\n')
                print(f'互补序列为： {task3_tools.hub(r)}\n')
                print(f'反向互补序列为： {task3_tools.fanx_hub(r)}\n')
                b = 0
            else:
                if re.match(new_a, eachline) != None:
                    b=1
                    print(f'序列id为： {eachline}')
