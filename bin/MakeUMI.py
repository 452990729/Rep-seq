#!/usr/bin/env python

import re
import os
import sys
import gzip
import json
from workflow import Json2Str

class Fastq(object):
    def __init__(self, list_in):
        list_tmp = re.split('\s+', list_in[0])
        self.index = re.split('\:', list_tmp[1])[-1]
        self.id = list_tmp[0]
        self.f = list_in[0]
        self.seq = list_in[1]
        self.t = list_in[2]
        self.q = list_in[3]

    def MakeFs(self, barcode, cut=15):
        seq_id = self.id+' '+'INDEX='+self.index+'|BARCODE='+barcode
        return '\n'.join([seq_id, self.seq[cut:],\
                          self.t, self.q[cut:]])


def HnadleFq(file_in):
    m = 0
    list_tmp = []
    base = re.split('\.', os.path.basename(file_in))[0]
    out = open(base+'_WithUMI.fastq', 'w+')
    with open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            m += 1
            if m == 4:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                out.write(ob.MakeFs(ob.seq[:15])+'\n')
                list_tmp = []
                m = 0
            else:
                list_tmp.append(line)

def main():
    HnadleFq(sys.argv[1])


if __name__ == '__main__':
    main()
    

