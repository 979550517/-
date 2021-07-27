#!/usr/bin/env python
# -*- coding: utf-8 -*-import argparse
from urllib.request import urlopen
import re
myURL = urlopen('ftp://ftp.ncbi.nlm.nih.gov/refseq/release/bacteria/')
for i in myURL:
    i=str(i)
    a=i.split(sep=' ')
    c=a[-1].split(sep='\\')
    moudel = 'bacteria.*.*.genomic.fna.gz'
    if re.match('bacteria.*.*.genomic.fna.gz',c[0]) != None:
        print(c[0])
    else:
        continue