#!/usr/bin/env python

import os
import sys
import re
import matplotlib
matplotlib.use('Agg')
import venn
#from matplotlib_venn import venn2
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

def main():
    l1, lb1 = HandleFq(sys.argv[1])
    l2, lb2 = HandleFq(sys.argv[2])
    labels = venn.get_labels([l1,l2],\
                            fill=['number',])
    fig, ax = venn.venn2(labels, names=[lb1,lb2])
    ax.set_title('Comparison of umis')
    plt.savefig('2wayvenn.png')


if __name__ == '__main__':
    main()
