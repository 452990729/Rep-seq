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
    labels = venn.get_labels([list1, list2], fill=['number',])
    fig, ax = venn.venn2(labels, names=[label1, label2])
    ax.set_title('Comparison of CDR3 between {} and {}'.format(label1, label2))
    plt.savefig('ComparisonCDR3Between{}and{}.png'.format(label1, label2))


if __name__ == '__main__':
    main()


