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

def GetData(inpath):
    root, dirs, files = next(os.walk(inpath))
    list_x = []
    list_y = []
    for dr in dirs:
        with open(os.path.join(root+'/'+dr, '.'.join([dr, 'VJCom.stat'])), 'r') as f:
            for line in f:
                list_split = re.split('\t', line)
                if list_split[0] not in list_y:
                    list_y.append(list_split[0])
                if list_split[1] not in list_x:
                    list_x.append(list_split[1])
    dict_sample = {}
    for dr in dirs:
        dict_tmp = {}
        with open(os.path.join(root+'/'+dr, '.'.join([dr, 'VJCom.stat'])), 'r') as f:
            for line in f:
                list_split = re.split('\t', line.strip())
                dict_tmp[','.join(list_split[:2])] = float(list_split[-1])
        list_tmp = []
        data = ''
        for y in list_y:
            list_tmp = []
            for x in list_x:
                gene = ','.join([y,x])
                if gene in dict_tmp:
                    list_tmp.append(dict_tmp[gene])
                else:
                    list_tmp.append(0.0)
            if len(data) == 0:
                data = np.array(list_tmp)
            else:
                data = np.vstack([data, np.array(list_tmp)])
        dict_sample[dr] = deepcopy(data)
    return dict_sample, list_x, list_y

def MakePic(dict_sample, list_x, list_y, list_group, outpath):
    fig, axs = plt.subplots(1, len(list_group), figsize=(12,5))
    m = 0
    for sample in list_group[:-1]:
        np_x = dict_sample[sample]
        ax = axs[m]
        im = ax.imshow(np_x, cmap="YlGnBu")
        ax.set_xticks(np.arange(np_x.shape[1]))
        ax.set_xticklabels(list_x)
        ax.tick_params(top=True, bottom=False, left=False, right=False,\
                       labeltop=True, labelbottom=False, labelleft=False, labelright=False)
        plt.setp(ax.get_xticklabels(), rotation=-90, ha="right",
                 rotation_mode="anchor", fontsize=3)
        for edge, spine in ax.spines.items():
            spine.set_visible(False)
        ax.set_xticks(np.arange(np_x.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(np_x.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.set_xlabel(sample)
        m += 1
    sample = list_group[-1]
    ax = axs[m]
    np_x = dict_sample[sample]
    im = ax.imshow(np_x, cmap="YlGnBu")
#    cbar = ax.figure.colorbar(im, ax=ax, orientation='vertical', fraction=0.04)
    ax.set_xticks(np.arange(np_x.shape[1]))
    ax.set_yticks(np.arange(np_x.shape[0]))
    ax.set_xticklabels(list_x)
    ax.set_yticklabels(list_y)
    ax.tick_params(top=True, bottom=False, left=False, right=True,\
                   labeltop=True, labelbottom=False, labelleft=False, labelright=True)
    plt.setp(ax.get_xticklabels(), rotation=-90, ha="right",
             rotation_mode="anchor", fontsize=3)
    plt.setp(ax.get_yticklabels(), fontsize=4)
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xticks(np.arange(np_x.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(np_x.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.set_xlabel(sample)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax = fig.add_axes([0.3,0.9,0.4,0.1])
    ax.figure.colorbar(im, ax=ax, orientation='horizontal', fraction=0.2)
    ax.tick_params(top=False, bottom=False, left=False, right=False,\
                   labeltop=False, labelbottom=False, labelleft=False, labelright=False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.savefig(outpath+'.pdf')
    plt.savefig(outpath+'.jpg', dpi=400)

def main():
    with open(sys.argv[2], 'r') as f:
        list_group = [i.strip() for i in f]
    dict_sample, list_x, list_y = GetData(sys.argv[1])
    MakePic(dict_sample, list_x, list_y, list_group, sys.argv[3])


if __name__ == '__main__':
    main()




