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

    def RepaclePrm(self, pos, seq_in):
        return '\n'.join([self.f, seq_in+self.seq[pos+20:], \
                self.t, self.q[pos:]])

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
        for i in range(4,7):
            if Dist(prm, seq_in[i:i+20], mismatch):
                a = 1
                return i,prm
    if a == 0:
        return 0, 0

def HnadleFq(file_in, dict_in, mismatch):
    m = 0
    list_tmp = []
    dict_tmp = {}
    list_key = dict_in.keys()
    base = re.split('_', os.path.basename(file_in))[0]
    for value in dict_in.values():
        locals()[value] = open(base+'_'+value+'_R2.fastq', 'w+')
    NoMatch = open(base+'_NoClassify_R2.fastq', 'w+')
    JsonOut = open(base+'_classify.json', 'w+')
    with gzip.open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            m += 1
            if m == 4:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                p, q = AlignPrm(ob.seq, list_key, mismatch)
                if p:
                    locals()[dict_in[q]].write(ob.RepaclePrm(p, q)+'\n')
                    dict_tmp[ob.id] = dict_in[q]
                else:
                    NoMatch.write(ob.fq+'\n')
                    dict_tmp[ob.id] = 'NoClassify'
                list_tmp = []
                m = 0
            else:
                list_tmp.append(line)
    JsonOut.write(json.dumps(dict_tmp))

def main():
    dict_fa = ReadFasta(sys.argv[1])
    HnadleFq(sys.argv[2], dict_fa, int(sys.argv[3]))


if __name__ == '__main__':
    main()
    

