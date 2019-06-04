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


def GetMutation(file_in, tp):
    list_tmp = []
    if tp == 'V':
        m = -10
    elif tp == 'J':
        m = -6
    with open(file_in, 'r') as in1:
        for line in in1.readlines()[1:]:
            list_split = re.split('\t', line.strip())
            if list_split[8]:
                mut = len(re.findall(r'[ATCG]{2}', list_split[m]))
                list_tmp.append(mut)
    return np.array(list_tmp)

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    cap = plt.cm.get_cmap(name, n+1)
    return [cap(i) for i in range(n)]


def MakePlot(list_np, list_label, outpath):
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
    plt.savefig(os.path.join(outpath, 'MutationFrequencyDistribution.png'))


def main():
    list_np = []
    list_label = []
    for i in sys.argv[2:-1]:
        list_np.append(GetMutation(i, sys.argv[1]))
        list_label.append(re.split('_', os.path.basename(i))[0])
    MakePlot(list_np, list_label, sys.argv[-1])


if __name__ == '__main__':
    main()


