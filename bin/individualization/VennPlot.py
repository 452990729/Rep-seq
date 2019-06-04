#!/usr/bin/env python

import os
import sys
import re
import matplotlib
matplotlib.use('Agg')
import venn
from matplotlib import pyplot as plt


def HandleFq(file_in):
    base = '_'.join(re.split('_', os.path.basename(file_in))[:2])
    list_tmp = []
    m = 0
    with open(file_in, 'r') as in1:
        for line in in1:
            m += 1
            if m%4 == 2:
                list_tmp.append(line.strip())
    return set(list_tmp), base

def ReadTab(file_in):
    list_tmp = []
    label = '_'.join(re.split('_', os.path.basename(file_in))[:2])
    with open(file_in, 'r') as in1:
        for line in in1.readlines()[1:]:
            list_tmp.append(re.split('\t', line.strip())[36])
    return set(list_tmp), label

def main():
    len_arg = len(sys.argv)
    if sys.argv[1] == 'fastq':
        func = HandleFq
    elif sys.argv[1] == 'tab':
        func = ReadTab
    list_l = []
    list_lb = []
    for i in range(len_arg-2):
        l, lb = func(sys.argv[i+2])
        list_l.append(l)
        list_lb.append(lb)
    labels = venn.get_labels(list_l, fill=['number',])
    if len_arg == 4:
        fig, ax = venn.venn2(labels, names=list_lb)
    elif len_arg == 5:
        fig, ax = venn.venn3(labels, names=list_lb)
    elif len_arg == 6:
        fig, ax = venn.venn4(labels, names=list_lb)
    elif len_arg == 7:
        fig, ax = venn.venn5(labels, names=list_lb)
    elif len_arg == 8:
        fig, ax = venn.venn6(labels, names=list_lb)
    plt.savefig('{}wayvenn.png'.format(str(len_arg-2)))


if __name__ == '__main__':
    main()
