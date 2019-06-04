#!/usr/bin/env python


import sys
import os
import re
import gzip

i = 0

base = re.split('\.', os.path.basename(sys.argv[1]))[0]
fumi = open(base+'_UMI.fastq', 'w+')
dict_tmp = {}

with open(sys.argv[1], 'r') as pd:
    for line in pd:
        line = line.strip()
        i += 1
        if i == 1:
            st = line
        elif i == 2:
            umi = line[:16]
            fumi.write(st+'+'+umi+'\n'+umi+'\n')
        elif i == 3:
            fumi.write(line+'\n')
        elif i == 4:
            fumi.write(line[:16]+'\n')
            i = 0

fumi.close()
