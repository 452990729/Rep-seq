#!/usr/bin/env python

import re
import os
import sys
import gzip
import json
from workflow import Json2Str

class Fastq(object):
    def __init__(self, list_in):
        self.id = re.split('\s+', list_in[0])[0]
        self.f = list_in[0]
        self.seq = list_in[1]
        self.t = list_in[2]
        self.q = list_in[3]

    def Correct(self, seq_in):
        return '\n'.join([self.f, seq_in+self.seq[15:],\
                self.t, self.q])


def HnadleFq(file_in, json_in):
    m = 0
    list_tmp = []
    with open(json_in, 'r') as in1:
        dict_tmp = Json2Str(json.load(in1))
    base = re.split('\.', os.path.basename(file_in))[0]
    out = open(base+'_CorrectUMI.fastq', 'w+')
    with open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            m += 1
            if m == 4:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                out.write(ob.Correct(dict_tmp[ob.id])+'\n')
                list_tmp = []
                m = 0
            else:
                list_tmp.append(line)

def main():
    HnadleFq(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
    

