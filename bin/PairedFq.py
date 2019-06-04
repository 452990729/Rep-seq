#!/usr/bin/env python

import re
import argparse

class Fastq(object):
    def __init__(self, list_in):
        self.id = re.split('\s+', list_in[0])[0]
        self.raw = '\n'.join(list_in)

def ReadFastq(file_in):
    '''
    read the fastq data -> dict[fastq.id]=Fastq(object)
    '''
    i = 0
    list_tmp = []
    dict_tmp = {}
    with open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            i += 1
            if i < 4:
                list_tmp.append(line)
            elif i == 4:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                dict_tmp[ob.id] = ob
                i = 0
                list_tmp = []
    return dict_tmp

def Paired(dict_s1, dict_s2, file_out1, file_out2):
    '''
    paired the seq
    write out the format fastq data
    '''
    set_ds = set(dict_s1.keys())&set(dict_s2.keys())
    out1 = open(file_out1, 'w+')
    out2 = open(file_out2, 'w+')
    i = 0
    for key in set_ds:
        out1.write(dict_s1[key].raw+'\n')
        out2.write(dict_s2[key].raw+'\n')
    out1.close()
    out2.close()

def ChangeName(string_in):
    '''
    change the output name
    return string
    '''
    list_tmp = re.split('\.', string_in)
    return '.'.join(list_tmp[:-1])+'_pairedfq-pass'+'.'+list_tmp[-1]

def main():
    parser = argparse.ArgumentParser(description="instead the PairSeq.py of\
                                     pRESTO pipeline")
    parser.add_argument('--f1',help="the fastq1", required=True)
    parser.add_argument('--f2',help="the fastq2", required=True)
    argv=vars(parser.parse_args())
    dict1 = ReadFastq(argv['f1'])
    dict2 = ReadFastq(argv['f2'])
    Paired(dict1, dict2, ChangeName(argv['f1']), ChangeName(argv['f2']))


if __name__ == '__main__':
    main()
