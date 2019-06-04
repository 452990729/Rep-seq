#!/usr/bin/env python

import sys
import re
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import venn

def ReadTab(file_in):
    list_tmp = []
    label = '_'.join(re.split('_', os.path.basename(file_in))[:2])
    with open(file_in, 'r') as in1:
        for line in in1.readlines()[1:]:
            list_tmp.append(re.split('\t', line.strip())[-12])
    return list_tmp, label

def main():
    list1, label1 = ReadTab(sys.argv[1])
    list2, label2 = ReadTab(sys.argv[2])
    set1 = set(list1)
    set2 = set(list2)
    a = 0
    b = 0
    c = 0
    d = 0
    for i in list1:
        if i in set2:
            b += 1
        else:
            a += 1
    for i in list2:
        if i in set1:
            d += 1
        else:
            c += 1
    print 'uniqa'+'\t'+str(a)
    print 'alla'+'\t'+str(b)
    print 'uniqb'+'\t'+str(c)
    print 'allb'+'\t'+str(d)

if __name__ == '__main__':
    main()


