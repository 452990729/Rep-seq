#!/usr/bin/env python2


import sys
import re


class Fastq(object):
    def __init__(self, list_in):
        list_tp = re.split('\s+', list_in[0])
        self.id = list_tp[0]
        self.seq = list_in[1]
        self.fq = '\n'.join(list_in)


def HandleFastq(file_in, file_out):
    i = 0
    set_t = set()
    list_tmp = []
    out = open(file_out, 'w+')
    with open(file_in, 'r') as f:
        for line in f:
            line = line.strip()
            i += 1
            if i%4 == 0:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                if ob.id not in set_t:
                    if len(ob.seq) > 1:
                        out.write(ob.fq+'\n')
                        set_t.add(ob.id)
                list_tmp = []
            else:
                list_tmp.append(line)
    out.close()

def main():
    HandleFastq(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
