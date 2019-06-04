#!/usr/bin/env python


import sys
import os
import re
from collections import Counter

class Tab(object):
    def __init__(self, line):
        list_split = re.split('\t', line.strip())
        self.cloneId = list_split[0]
        self.cloneCount = list_split[1]
        self.bestVGene = list_split[3]
        self.bestDGene = list_split[4]
        self.bestJGene = list_split[5]
        self.nSeqCDR3 = list_split[-2]
        self.aaSeqCDR3 = list_split[-1]
        self.line  = line.strip()

    def IsFunctional(self):
        if len(self.nSeqCDR3)%3 == 0 and ('*' not in self.aaSeqCDR3) and \
           len(self.aaSeqCDR3) >=4:
            return True

def ReadTab(file_in, outpath):
    base = re.split('\.', os.path.basename(file_in))[0]
    out = open(os.path.join(outpath, base+'.CloneFilter.txt'), 'w+')
    with open(file_in, 'r') as in1:
        list_in = in1.readlines()
        title = list_in[0].strip()
        out.write(title+'\n')
        for line in list_in[1:]:
            ob = Tab(line)
            if ob.IsFunctional():
                out.write(ob.line+'\n')
    out.close()

def main():
    ReadTab(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
