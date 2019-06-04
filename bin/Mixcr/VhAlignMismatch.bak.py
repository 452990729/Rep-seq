#!/usr/bin/env python

import sys
import re
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from scipy import stats


def GetMutation(file_in):
    list_tp = ['D', 'I', 'S']
    list_tmp = []
    with open(file_in, 'r') as in1:
        for line in in1:
            s = re.split('\t', line.strip())[3]
            i = 0
            for tp in list_tp:
                i += s.count(tp)
            list_tmp.append(i)
    return np.array(list_tmp)

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    cap = plt.cm.get_cmap(name, n+1)
    return [cap(i) for i in range(n)]


def MakePlot(list_np, list_label):
    fig, axe = plt.subplots()
    colorp = get_cmap(len(list_np))
    i = 0
    for data in list_np:
        values, base = np.histogram(data, bins=40)
        tl = sum(values)
        vs = [round(float(m)*100/tl, 2) for m in values]
        cumulative = np.cumsum(vs)
        axe.plot(base[:-1], cumulative, c=colorp[i])
        i += 1
    patch = [mpatches.Patch(color=colorp[i], label=list_label[i]) for\
            i in range(len(list_np))]
    if len(list_np) == 2:
        (d,p) = stats.ks_2samp(list_np[0], list_np[1])
        if p <0.0001:
            axe.annotate('****', (25,70))
        elif  p <0.001:
            axe.annotate('***', (25,70))
#        axe.annotate('p='+str(p), (15,90))

    axe.legend(handles=patch)
    axe.set_title('Cumulative frequency distribution of somatic mutations')
    axe.set_xlabel('Number of mutations')
    axe.set_ylabel('Cumulative frequency(%)')
    axe.set_xlim(-1, 40)
    axe.spines['right'].set_visible(False)
    axe.spines['top'].set_visible(False)
    plt.savefig('MutationFrequencyDistribution.png')


def main():
    list_np = []
    list_label = []
    for i in sys.argv[1:]:
        list_np.append(GetMutation(i))
        list_label.append(re.split('\.', os.path.basename(i))[0])
    MakePlot(list_np, list_label)


if __name__ == '__main__':
    main()


