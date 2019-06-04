#!/usr/bin/env python

import re
import sys
import gzip
import os
import json
from workflow import Dist

class Fastq(object):
    def __init__(self, list_in):
        self.id = re.split('\s+', list_in[0])[0]
        self.f = list_in[0]
        self.seq = list_in[1]
        self.t = list_in[2]
        self.q = list_in[3]
        self.fq = '\n'.join(list_in)

    def CutP(self, pos, prm):
        return '\n'.join([self.f, self.seq[pos+len(prm):], \
                self.t, self.q[pos+len(prm):]])

def ReadFasta(file_in):
    dict_tmp = {}
    with open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            if line.startswith('>'):
                af = line.lstrip('>')
            else:
                dict_tmp[line] = af
    return dict_tmp

def AlignPrm(seq_in, list_in, mismatch):
    a = 0
    for prm in list_in:
        for i in range(0,5):
            if Dist(prm, seq_in[i:i+len(prm)], mismatch):
                a = 1
                return i, prm
    if a == 0:
        return 0, 0

dict_tmp = {}
def HnadleFq(file_in, dict_in, mismatch, handle=0):
    global dict_tmp
    m = 0
    list_tmp = []
    list_key = dict_in.keys()
    with gzip.open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            m += 1
            if m == 4:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                p, q = AlignPrm(ob.seq, list_key, mismatch)
                if q:
                    dict_tmp[ob.id] = dict_in[q]
                elif handle:
                    pass
                else:
                    dict_tmp[ob.id] = 'NoClassify'
                list_tmp = []
                m = 0
            else:
                list_tmp.append(line)

def WriteFile(dict_in, file_in):
    list_fl = set(dict_in.values())
    m = 0
    list_tmp = []
    base = re.split('\.', os.path.basename(file_in))[0]
    for value in list_fl:
        locals()[value] = open(value+'_'+base+'.fastq', 'w+')
    with gzip.open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            m += 1
            if m == 4:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                locals()[dict_in[ob.id]].write(ob.fq+'\n')
                list_tmp = []
                m = 0
            else:
                list_tmp.append(line)
    for value in list_fl:
        locals()[value].close()
        os.system('gzip {}'.format(value+'_'+base+'.fastq'))

def main():
    global dict_tmp
    dict_fa = ReadFasta(sys.argv[1])
    HnadleFq(sys.argv[2], dict_fa, int(sys.argv[4]))
    HnadleFq(sys.argv[3], dict_fa, int(sys.argv[4]), 1)
    WriteFile(dict_tmp, sys.argv[2])
    WriteFile(dict_tmp, sys.argv[3])

if __name__ == '__main__':
    main()

