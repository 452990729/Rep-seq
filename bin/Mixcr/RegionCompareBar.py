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

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    cap = plt.cm.get_cmap(name, n+1)
    return [cap(i) for i in range(n)]


def MakePlot(x, list_y, list_label, tp):
    fig, axe = plt.subplots()
    colorp = get_cmap(len(list_y))
    i = 0
    width = 0.25
    xu = np.arange(1, len(x)+1)
    for y in list_y:
        axe.bar(xu+i*width, y, width, color=colorp[i])
        i += 1
    patch = [mpatches.Patch(color=colorp[i], label=list_label[i])\
             for i in range(len(list_y))]
    axe.legend(handles=patch)
#    axe.set_xlabel('{} genes'.format(tp))
    axe.set_ylabel('Percentage(%)')
    axe.set_xticks(xu)
    axe.set_xticklabels(x)
#    for label in axe.get_yticklabels():
#        label.set_fontsize(30)
    axe.spines['right'].set_visible(False)
    axe.spines['top'].set_visible(False)
    plt.savefig('ClassifyBar.png', dpi=100)


def main():
    list_dict = []
    list_label = []
    dict_tmp = {}
    list_y = []
    for i in sys.argv[1:]:
        with open(i, 'r') as in1:
            for line in in1:
                list_split = re.split('\s+', line.strip())
                dict_tmp[list_split[0]] = list_split[-1]
        list_dict.append(dict_tmp)
        list_label.append(re.split('\.', os.path.basename(i))[0])
        dict_tmp = {}
    tp = re.split('\.', os.path.basename(sys.argv[1]))[1]
    x = sorted(set(reduce(lambda x,y:x+y, [i.keys() for i in list_dict])))
    for i in x:
        for dt in list_dict:
            if i not in dt:
                dt[i] = 0.0
    for dt in list_dict:
        list_y.append(np.array([dt[i] for i in x]))
    MakePlot(x, list_y, list_label, tp)


if __name__ == '__main__':
    main()


