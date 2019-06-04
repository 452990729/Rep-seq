#!/usr/bin/env python2

import sys
import re

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from scipy import stats


def HandleClone(file_in):
    dict_clone = {}
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            list_split = re.split('\t', line.strip())
            if list_split[-4] not in dict_clone:
                dict_clone[list_split[-4]] = int(list_split[-2])
            else:
                dict_clone[list_split[-4]] += int(list_split[-2])
    tl = sum(dict_clone.values())
    return {key:round(float(dict_clone[key])/tl, 6) for key in dict_clone},\
            re.split('_', re.split('\/', file_in)[-1])[0]

def CompareClone(dict1, dict2):
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
    return x,y,colors

def ScatterPlot(list_in):
    shape = re.split(r':', list_in[-1])
    fig, ax = plt.subplots(int(shape[0]), int(shape[1]), figsize=(12, 12))
    list_ax = reduce(lambda x,y:x+y, [list(m) for m in list(ax)])
    i = 0
    for m in list_in[:-1]:
        list_split = re.split(r':', m)
        dict1,lb1 = HandleClone(list_split[0])
        dict2,lb2 = HandleClone(list_split[1])
        x,y,colors = CompareClone(dict1, dict2)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        base = (int(max(x.max(), y.max())*100)+1)*0.01
        list_ax[i].scatter(x, y, c=colors, alpha=0.5)
        list_ax[i].set_xlim(-1e-6, 1e-2+1e-4)
        list_ax[i].set_ylim(-1e-6, 1e-2+1e-4)
        list_ax[i].set_xlabel(lb1)
        list_ax[i].set_ylabel(lb2)
        list_ax[i].set_xticks([0, 1e-2])
        list_ax[i].set_xticklabels(['0', '1e-2'])
        list_ax[i].set_yticks([0, 1e-2])
        list_ax[i].set_yticklabels(['0', '1e-2'])
        list_ax[i].set_title('$r^{2}$ = '+str(round(r_value, 3)))
        i += 1
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    plt.savefig('SampleRepeatability.pdf', dpi=100)

def main():
    ScatterPlot(sys.argv[1:])


if __name__ == '__main__':
    main()
