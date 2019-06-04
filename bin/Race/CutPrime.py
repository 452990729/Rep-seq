#!/usr/bin/env python

import re
import sys
import os
import gzip
from workflow import Dist
from workflow import HandleDegenerateBase

class Fastq(object):
    def __init__(self, list_in):
        self.id = re.split('\s+', list_in[0])[0]
        self.f = list_in[0]
        self.seq = list_in[1]
        self.t = list_in[2]
        self.q = list_in[3]
        self.fq = '\n'.join(list_in)

    def CutP(self, length, start):
        return '\n'.join([self.f, self.seq[start+length:],\
                         self.t, self.q[start+length:]])


def HandlePrime(file_in):
    with open(file_in, 'r') as in1:
        list_fa = filter(lambda x:not x.startswith('>'),\
                         [i.strip() for i in in1])
    dict_tmp = {}
    for fa in list_fa:
        if len(fa) not in dict_tmp:
            dict_tmp[len(fa)] = HandleDegenerateBase(fa)
        else:
            dict_tmp[len(fa)] += HandleDegenerateBase(fa)
    return dict_tmp, sorted(dict_tmp.keys(), reverse=True)

def AlignPrm(seq_in, dict_in, mismatch, start, list_len):
    a = 0
    for i in list_len:
        for prm in dict_in[i]:
            if Dist(prm, seq_in[start:start+i], mismatch):
                a = 1
                return i
    if a == 0:
        return 0

def HnadleFq(file_in, dict_fa, list_len, mismatch, flout):
    m = 0
    list_tmp = []
    dict_tmp = {}
    out = open(flout, 'w+')
    if file_in.endswith('gz'):
        in1 = gzip.open(file_in, 'r')
    else:
        in1 = open(file_in, 'r')
    for line in in1:
        line = line.strip()
        m += 1
        if m == 4:
            list_tmp.append(line)
            ob = Fastq(list_tmp)
            for start in range(1,9):
                p = AlignPrm(ob.seq, dict_fa, mismatch, start, list_len)
                if p:
                    out.write(ob.CutP(p, start)+'\n')
                    break
            list_tmp = []
            m = 0
        else:
            list_tmp.append(line)
    in1.close()
    out.close()

def main():
    dict_fa, list_len = HandlePrime(sys.argv[1])
    HnadleFq(sys.argv[2], dict_fa, list_len, 2, sys.argv[3])


if __name__ == '__main__':
    main()
