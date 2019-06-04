#!/usr/bin/env python

import os
import sys
import re
import matplotlib
matplotlib.use('Agg')
from matplotlib_venn import venn2
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
    set1, lb1 = ReadTab(sys.argv[2], sys.argv[1])
    set2, lb2 = ReadTab(sys.argv[3], sys.argv[1])
    venn2([set1, set2], (lb1, lb2))
    plt.savefig('{}Venn.png'.format(sys.argv[1]))


if __name__ == '__main__':
    main()
