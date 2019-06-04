#!/usr/bin/env python

import sys
import re
import os
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt


def GetMutation(file_in, tp):
    list_tp = ['D', 'I', 'S']
    list_tmp = []
    m = 0
    with open(file_in, 'r') as in1:
        for line in in1:
            if line.startswith(tp):
                m += 1
                s = re.split('\t', line.strip())[3]
                i = 0
                for ts in list_tp:
                    i += s.count(ts)
                list_tmp.append(i)
    list_tmp = sorted(dict(Counter(list_tmp)).items(), key=lambda x:x[0])
    return [np.array([i[0] for i in list_tmp]),\
            np.array([round(float(i[1])*100/m, 2) for i in list_tmp])]

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    cap = plt.cm.get_cmap(name, n+1)
    return [cap(i) for i in range(n)]


def MakePlot(list_np, list_label, lb):
    fig, axe = plt.subplots()
    colorp = get_cmap(len(list_np))
    i = 0
    for data in list_np:
        x,y = data[0],data[1]
        axe.plot(x, y, c=colorp[i])
        i += 1
    patch = [mpatches.Patch(color=colorp[i], label=list_label[i]) for\
            i in range(len(list_np))]
    axe.legend(handles=patch)
    axe.set_title('Comparison of {} mutation'.format(lb))
    axe.set_xlabel('Number of mutations')
    axe.set_ylabel('% of total')
    axe.set_xlim(-1, 40)
    axe.spines['right'].set_visible(False)
    axe.spines['top'].set_visible(False)
    plt.savefig('{}MutationFrequencyDistribution.png'.format(lb))


def main():
    list_np = []
    list_label = []
    for fl in sys.argv[1:-1]:
        list_np.append(GetMutation(fl, sys.argv[-1]))
        list_label.append(re.split('\.', os.path.basename(fl))[0])
    MakePlot(list_np, list_label, sys.argv[-1])


if __name__ == '__main__':
    main()


