#!/usr/bin/env python

import sys
import re
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from scipy import stats


def ReadTab(file_in):
    dict_tmp = {}
    label = re.split('\.', os.path.basename(file_in))[0]
    with open(file_in, 'r') as in1:
        for line in in1:
            list_split = re.split('\s+', line.strip())
            dict_tmp['|'.join(list_split[:-2])] = int(list_split[-2])
    tal = sum(dict_tmp.values())
    return {key:round(float(value)/tal, 4) for key,value in \
            dict_tmp.items()}, label

def ScatterPlot(dict1, dict2, label1, label2, tp, outpath):
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
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    base = (int(max(x.max(), y.max())*100)+1)*0.01
    if tp != 'VDJ':
        for i, txt in enumerate(keys):
            if abs(x[i]-y[i]) >= 0.2*base:
                ax.annotate(txt, (x[i],y[i]))
    ax.annotate('$R^{2}$ = '+str(round(r_value, 3)), (0.3*base,0.9*base))
    m, b = np.polyfit(x, y, 1)
    ax.plot(x, m*x + b, '-')
    ax.set_xlim(-0.001, base)
    ax.set_ylim(-0.001, base)
    ax.set_xlabel(label1)
    ax.set_ylabel(label2)
    ax.set_title('Comparison of {} between {} and {}'.format(tp, label1, label2))
    plt.savefig(os.path.join(outpath, \
                'ComparisonOf{}Between{}and{}.png'.format(tp, label1, label2)))

def main():
    dict1, label1 = ReadTab(sys.argv[2])
    dict2, label2 = ReadTab(sys.argv[3])
    ScatterPlot(dict1, dict2, label1, label2, sys.argv[1], sys.argv[4])


if __name__ == '__main__':
    main()


