#!/usr/bin/env python

import re
from glob import glob
import os
import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    cap = plt.cm.get_cmap(name, n+1)
    return [cap(i) for i in range(n)]

def PlotQC(paths, xlb):
    list_tab = []
    label = []
    for path in paths:
        list_tab.append(os.path.join(path, 'QC_table.tab'))
        ls = re.split('\/', path)[-2]
        label.append(ls)
    list_np = []
    medians = []
    fig, axes = plt.subplots()
    for path in list_tab:
        np_tmp = np.loadtxt(path, dtype='S10')
        np_in = np_tmp[1:10000, 1].astype('float')
        list_np.append(np_in)
        medians.append(np.median(np_in))
    vplot = axes.violinplot(list_np, showmeans=False,\
            showmedians=False, showextrema=False, widths=0.2)
    bplot = axes.boxplot(list_np, vert=True, patch_artist=True,\
            showfliers=False, widths=0.03, medianprops={'linestyle': 'None'})
    inds = np.arange(1, len(medians)+1)
    axes.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)
    for patch in bplot['boxes']:
        patch.set_facecolor('black')
    for patch, color in zip(vplot['bodies'], get_cmap(len(label))):
        patch.set_color(color)
    axes.set_xticks([y+1 for y in range(len(label))], )
    axes.set_xlabel(xlb)
    axes.set_ylabel('Value')
    axes.set_xticklabels(label)
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.set_title('Distribution of Reads Quality')
    plt.savefig('ReadsQuality({}).png'.format(xlb))

def main():
    path_l = re.split('\,', sys.argv[1])
    PlotQC(path_l, sys.argv[2])


if __name__ == '__main__':
    main()

