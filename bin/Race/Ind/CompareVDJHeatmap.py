#!/usr/bin/env python2


import sys
import os
import re
from copy import deepcopy
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import Heatmap

def GetData(inpath, tp):
    root, dirs, files = next(os.walk(inpath))
    list_tmp = []
    for dr in dirs:
        with open(os.path.join(root+'/'+dr, '.'.join([dr, tp, 'stat'])), 'r') as f:
            for line in f:
                list_tmp.append(re.split('\t', line)[0])
    list_gene = list(set(list_tmp))
    dict_sample = {}
    for dr in dirs:
        dict_tmp = {}
        with open(os.path.join(root+'/'+dr,\
                               '.'.join([dr, tp, 'stat'])), 'r') as f:
            for line in f:
                list_split = re.split('\t', line.strip())
                dict_tmp[list_split[0]] = float(list_split[-1])
        list_tmp = []
        for gene in list_gene:
            if gene in dict_tmp:
                list_tmp.append(dict_tmp[gene])
            else:
                list_tmp.append(0.0)
        dict_sample[dr] = deepcopy(list_tmp)
    return dict_sample, list_gene

def MakePic(dict_sample, list_gene, list_group, tp, outpath):
    np_x = ''
    for i in list_group:
        if len(np_x) == 0:
            np_x = np.array(dict_sample[i])
        else:
            np_x = np.vstack([np_x, np.array(dict_sample[i])])
    fig, ax = plt.subplots()
    im, cbar = Heatmap.heatmap(np_x, list_group, list_gene, ax,\
                              cmap="YlGnBu")
    plt.savefig(os.path.join(outpath, 'ComparisonOf{}Gene.pdf'.format(tp)))
    plt.savefig(os.path.join(outpath, 'ComparisonOf{}Gene.jpg'.format(tp)),\
               dpi=300)

def main():
    list_tp = ['V', 'D', 'J']
    with open(sys.argv[2], 'r') as f:
        list_group = [i.strip() for i in f]
    for tp in list_tp:
        dict_sample, list_gene = GetData(sys.argv[1], tp)
        MakePic(dict_sample, list_gene, list_group, tp, sys.argv[3])


if __name__ == '__main__':
    main()




