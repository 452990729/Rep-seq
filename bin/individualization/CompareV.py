#!/usr/bin/env python

import sys
import re
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def ReadTab(file_in):
    dict_tmp = {}
    label = re.split('\.', os.path.basename(file_in))[0]
    with open(file_in, 'r') as in1:
        for line in in1:
            list_split = re.split('\t', line.strip())
            dict_tmp[list_split[0]] = int(list_split[1])
    tal = sum(dict_tmp.values())
    return {key:round(float(value)/tal, 2) for key,value in \
            dict_tmp.items()}, label

def ScatterPlot(dict1, dict2, label1, label2):
    fig, ax = plt.subplots()
    keys = set(dict1.keys())|set(dict2.keys())
    x = np.zeros(len(keys))
    y = np.zeros(len(keys))
    colors = np.random.rand(len(keys))
    i = 0
    for key in keys:
        if key in dict1:
            x[i] = dict1[key]
        if key in dict2:
            y[i] = dict2[key]
        i += 1
    ax.scatter(x, y, c=colors, alpha=0.5)
    for i, txt in enumerate(keys):
        ax.annotate(txt, (x[i],y[i]))
    m, b = np.polyfit(x, y, 1)
    ax.plot(x, m*x + b, '-')
    ax.set_xlim(-0.05, 0.2)
    ax.set_ylim(-0.05, 0.2)
    ax.set_xlabel(label1)
    ax.set_ylabel(label2)
    ax.set_title('Comparison of V gene between {} and {}'.format(label1, label2))
    plt.savefig('ComparisonOfVBetween{}and{}.png'.format(label1, label2))

def main():
    dict1, label1 = ReadTab(sys.argv[1])
    dict2, label2 = ReadTab(sys.argv[2])
    ScatterPlot(dict1, dict2, label1, label2)


if __name__ == '__main__':
    main()


