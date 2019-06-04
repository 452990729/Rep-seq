#!/usr/bin/env python

import sys
import os
import re


label = re.split('\.', os.path.basename(sys.argv[1]))[0]
out = open(os.path.join(sys.argv[2], label+'.alakazam.out'), 'w+')
out.write('\t'.join(['ID', 'CLONE', 'SAMPLE'])+'\n')
i = 0
with open(sys.argv[1], 'r') as in1:
    for line in in1.readlines()[1:]:
        i += 1
        list_tmp = re.split('\t', line.strip())
        for i in xrange(int(round(float(list_tmp[1]),0))):
            out.write(str(i)+'\t'+list_tmp[0]+'\t'+label+'\n')
out.close()
