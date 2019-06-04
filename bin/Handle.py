#!/usr/bin/env python

import re
import os
import sys
import gzip
import json
from workflow import Json2Str

class Fastq(object):
    def __init__(self, list_in):
        self.f = list_in[0]
        self.seq = list_in[1]
        self.t = list_in[2]
        self.q = list_in[3]

    def Correct(self):
        a = len(self.seq)-len(self.q)
        if a:
            q = self.q+','*a
        else:
            q = self.q
        return '\n'.join([self.f, self.seq,\
                self.t, q])


def HnadleFq(file_in):
    m = 0
    list_tmp = []
    with open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            m += 1
            if m == 4:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                print ob.Correct()
                list_tmp = []
                m = 0
            else:
                list_tmp.append(line)

def main():
    HnadleFq(sys.argv[1])


if __name__ == '__main__':
    main()
    

