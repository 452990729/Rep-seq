#!/usr/bin/env python

import os
import sys
import re
import matplotlib
matplotlib.use('Agg')
import venn
from matplotlib import pyplot as plt

def ReadTab(file_in, tp):
    if tp == 'n':
        num = -2
    elif tp == 'a':
        num = -1
    list_tmp = []
    label = re.split('\.', os.path.basename(file_in))[0]
    with open(file_in, 'r') as in1:
        for line in in1.readlines()[1:]:
            list_tmp.append(re.split('\t', line.strip())[num])
    return set(list_tmp), label

def main():
    len_arg = len(sys.argv)-1
    list_l = []
    list_lb = []
    for i in range(len_arg-2):
        l, lb = ReadTab(sys.argv[i+2], sys.argv[1])
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
    plt.savefig(os.path.join(sys.argv[-1],\
                             '{}2venn.png'.format(sys.argv[1])))
    plt.savefig(os.path.join(sys.argv[-1],\
                            '{}2venn.pdf'.format(sys.argv[1])))


if __name__ == '__main__':
    main()
