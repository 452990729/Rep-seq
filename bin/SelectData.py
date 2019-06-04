#!/usr/bin/env python

import re
import sys
import os
import json


class Fastq(object):
    def __init__(self, list_in):
        self.f = list_in[0]
        self.seq = list_in[1]
        self.t = list_in[2]
        self.q = list_in[3]
        self.fq = '\n'.join(list_in)
        list_split = re.split('\s+', list_in[0])
        self.id = list_split[0]
        self.barcode = re.split('\=', list_split[1])[-1]

class Select(object):
    def __init__(self, umi):
        self.umi = umi
        self.number = 0
        self.tal = []

    def UpdateNum(self):
        self.number += 1

    def UpdateTal(self, ob_in):
        self.tal += [ob_in]

    def WriteFq(self):
        return '\n'.join([i.fq for i in self.tal])

def HandleFq(file_in):
    dict_umi = {}
    list_tmp = []
    base = re.split('\.', os.path.basename(file_in))[0]
    out = open(base+'_select.fastq', 'w+')
    m = 0
    with open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            m += 1
            if m == 4:
                list_tmp.append(line)
                ob_fq = Fastq(list_tmp)
                if ob_fq.barcode not in dict_umi:
                    ob_umi = Select(ob_fq.barcode)
                    ob_umi.UpdateNum()
                    ob_umi.UpdateTal(ob_fq)
                    dict_umi[ob_fq.barcode] = ob_umi
                else:
                    ob_tmp = dict_umi[ob_fq.barcode]
                    ob_tmp.UpdateNum()
                    if ob_tmp.number <= 100:
                        ob_tmp.UpdateTal(ob_fq)
                list_tmp = []
                m = 0
            else:
                list_tmp.append(line)
    dict_num = {}
    for record in dict_umi:
        out.write(dict_umi[record].WriteFq()+'\n')
        dict_num[record] = dict_umi[record].number
    out.close()
    with open(base+'_select.json', 'w+') as outj:
        outj.write(json.dumps(dict_num))

def main():
    HandleFq(sys.argv[1])


if __name__ == '__main__':
    main()

