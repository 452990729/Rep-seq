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
        self.fq = '\n'.join(list_in)

def HnadleFq(file_in, json_in):
    m = 0
    list_tmp = []
    with open(json_in, 'r') as in1:
        dict_tmp = Json2Str(json.load(in1))
    base = re.split('_', os.path.basename(file_in))[0]
    set_keys = set(dict_tmp.keys())
    for value in set(dict_tmp.values()):
        locals()[value] = open(base+'_'+value+'_R1.fastq', 'w+')
    NoMatch = open(base+'_NoClassify_R1.fastq', 'w+')
    with gzip.open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            m += 1
            if m == 4:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                if ob.id in set_keys:
                    locals()[dict_tmp[ob.id]].write(ob.fq+'\n')
                else:
                    NoMatch.write(ob.fq+'\n')
                list_tmp = []
                m = 0
            else:
                list_tmp.append(line)

def main():
    HnadleFq(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
    

