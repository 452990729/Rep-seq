#!/usr/bin/env python

import sys
import re
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib_venn import venn2

def ReadTab(file_in):
    list_tmp = []
    label = '_'.join(re.split('_', os.path.basename(file_in))[:2])
    with open(file_in, 'r') as in1:
        for line in in1.readlines()[1:]:
            list_tmp.append(re.split('\t', line.strip())[-12])
    return set(list_tmp), label

def VennPlot(set1, set2, label1, label2):
    fig, ax = plt.subplots()
    venn2([set1, set2], (label1,label2))
    ax.set_title('Comparison of CDR3 between {} and {}'.format(label1, label2))
    plt.savefig('ComparisonCDR3Between{}and{}.png'.format(label1, label2))

def main():
    set1, label1 = ReadTab(sys.argv[1])
    set2, label2 = ReadTab(sys.argv[2])
    VennPlot(set1, set2, label1, label2)


if __name__ == '__main__':
    main()


