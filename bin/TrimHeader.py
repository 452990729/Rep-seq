#!/usr/bin/env python

import re
import sys

m = 0
out = open(re.split('\.', sys.argv[1])[0]+'_trim.fastq', 'w+')
with open(sys.argv[1], 'r') as in1:
    for line in in1:
        line = line.strip()
        m += 1
        if m%4 == 1:
            out.write(re.split('\s+', line)[0]+'\n')
        else:
            out.write(line+'\n')

out.close()
