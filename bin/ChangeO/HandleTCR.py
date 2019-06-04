#!/usr/bin/env python

import argparse
import re


class TabData(object):
    '''
    handle the changeo paserdb output
    '''
    def __init__(self, line_in):
        list_split = re.split('\t', line_in)
        self.id = list_split[0]
        self.cdr3 = list_split[-3]
        self.vcall = list_split[7]
        self.line = line_in

#    def AddClone(num_in):
#        return self.line+'\t'+str(num_in)

    def __eq__(self, other):
        if self.id == other.id:
            return True

    def __hash__(self):
        return 0

def ReadTab(file_in):
    with open(file_in, 'r') as in1:
        list_f = in1.readlines()
    header = list_f[0].strip()+'\t'+'CLONE'
    list_re = []
    i = 0
    for line in list_f[1:]:
        ob = TabData(line.strip())
        if ob not in list_re:
            m = 0
            for ref in list_re:
                if ob.cdr3 == ref.cdr3:
                    ob.clone = ref.clone
                    list_re.append(ob)
                    m = 1
                    break
            if m == 0:
                i += 1
                ob.clone = i
                list_re.append(ob)
    return header, list_re

def main():
    parser = argparse.ArgumentParser(description="clone the tcr file")
    parser.add_argument('--in',help="the input changeO tab file", required=True)
    argv=vars(parser.parse_args())
    header, list_re = ReadTab(argv['in'])
    base = re.split('\.', argv['in'])[0]
    out = open(base+'_clone-pass.tab', 'w+')
    out.write(header+'\n')
    for ob in list_re:
        out.write(ob.line+'\t'+str(ob.clone)+'\n')


if __name__ == '__main__':
    main()



