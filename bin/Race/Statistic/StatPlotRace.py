#!/usr/bin/env python

import re
from glob import glob
import os
import sys
import random
from copy import deepcopy
from collections import Counter
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
    list_tmp = [cap(i) for i in range(n)]
    random.shuffle(list_tmp)
    return list_tmp

def PlotCDR3(list_path, xlb, tp):
    paths = []
    if tp == 'n':
        for path in list_path:
            paths += glob(path+'/*.nCDR3.len.stat')
        st = 'Distribution of CDR3 Length(Nucleotide)'
        sf = 'CDR3LengthOfNucleotide.png'
        ylim = 90
    elif tp == 'a':
        for path in list_path:
            paths += glob(path+'/*.aCDR3.len.stat')
        st = 'Distribution of CDR3 Length(Amino)'
        sf = 'CDR3LengthOfAmino.png'
        ylim = 30
    label = []
    list_np = []
    medians = []
    fig, axes = plt.subplots()
    for path in paths:
        np_tmp = np.loadtxt(path, dtype='S10')
        np_in = np_tmp[:, 1].astype('int')
        list_np.append(np_in)
        medians.append(np.median(np_in))
        label.append(re.split('\.', os.path.basename(path))[0])
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
    axes.set_ylabel('Length(bp)')
    axes.set_xticklabels(label)
    axes.set_ylim(0, ylim)
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.set_title(st)
    plt.savefig(sf)

def PlotCDR3Bar(list_path, tp, pathout):
    paths = []
    if tp == 'n':
        for path in list_path:
            paths += glob(path+'/*.nCDR3.len.stat')
        st = 'Distribution of CDR3 Length(Nucleotide)'
        sf = 'CDR3LengthOfNucleotide.png'
        xlim = 120
    elif tp == 'a':
        for path in list_path:
            paths += glob(path+'/*.aCDR3.len.stat')
        st = 'Distribution of CDR3 Length(Amino)'
        sf = 'CDR3LengthOfAmino.png'
        xlim = 40
    if len(list_path) == 2:
        colors = ['g','r']
        fig, axes = plt.subplots()
        m = 0
        labels = []
        for path in sorted(paths):
            np_tmp = np.loadtxt(path, dtype='S10')
            np_in = np_tmp[:, 1].astype('int')
            label = re.split('\.', os.path.basename(path))[0]
            dict_tmp = dict(Counter(list(np_in)))
            keys = sorted(dict_tmp.keys())
            x = np.array(keys)
            tl = len(np_in)
            y = np.array([round(float(dict_tmp[i])*100/tl, 2) for i in keys])
            axes.bar(x, y, width=0.8, align='center', color=colors[m], alpha=0.4, label=label)
            m += 1
        axes.legend(loc='upper right')
        axes.set_xlim(0, xlim)
        axes.set_xlabel('Length')
        axes.set_ylabel('Pecentage (%)')
        axes.spines['right'].set_visible(False)
        axes.spines['top'].set_visible(False)
        axes.set_title(st)
    else:
        colors = get_cmap(len(list_path))
        if len(list_path)%2 == 0:
            fig, axes = plt.subplots(nrows=len(list_path)/2, ncols=2, figsize=(10, len(list_path)), dpi=300)
            handle = len(paths)/2
        else:
            fig, axes = plt.subplots(nrows=len(list_path)/2+1, ncols=2, figsize=(10, (len(list_path)/2+1)*2), dpi=300)
            axes[-1,-1].spines['right'].set_visible(False)
            axes[-1,-1].spines['left'].set_visible(False)
            axes[-1,-1].spines['top'].set_visible(False)
            axes[-1,-1].spines['bottom'].set_visible(False)
            axes[-1,-1].set_xticks([])
            axes[-1,-1].set_yticks([])
            handle = len(paths)/2+1
        m = 0
        n = 0
        c = 0
        for path in sorted(paths):
            np_tmp = np.loadtxt(path, dtype='S10')
            np_in = np_tmp[:, 1].astype('int')
            label = re.split('\.', os.path.basename(path))[0]
            dict_tmp = dict(Counter(list(np_in)))
            keys = sorted(dict_tmp.keys())
            x = np.array(keys)
            tl = len(np_in)
            y = np.array([round(float(dict_tmp[i])*100/tl, 2) for i in keys])
            axes[m, n].bar(x, y, width=0.8, align='center', color=colors[c],\
                     alpha=0.8, label=label)
            axes[m, n].legend(loc='upper right')
            axes[m, n].set_xlim(0, xlim)
#            axes[m ,n].set_xlabel('Length')
            axes[m, n].spines['right'].set_visible(False)
            axes[m, n].spines['top'].set_visible(False)
            c += 1
            if c < handle:
                m += 1
                d = deepcopy(m)
#                axes[m, n].set_ylabel('Pecentage (%)')
            else:
                m = c-d-1
                n = 1
#        axes[0, 0].set_ylabel('Pecentage (%)')
    fig.subplots_adjust(hspace=0.4)
    plt.savefig(os.path.join(pathout, sf))

def PlotVDJ(path_in, xlb):
    fig, ax = plt.subplots(2,2)
    axs = ax.flatten()
    def PlotPie(np_in, ax_in, ns):
        nps = np_in[:,1].astype('int')
        porcent = 100.*nps/nps.sum()
        patches, texts = ax_in.pie(nps, colors=get_cmap(len(np_in[:,0])),\
                shadow=True, startangle=90)
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(np_in[:,0], porcent)]
        if len(labels) <= 6:
            ax_in.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.9, 0.5),
                    fontsize=8)
        else:
            ax_in.legend(patches[:6], labels[0:], loc='center left', bbox_to_anchor=(-0.9, 0.5),
                    fontsize=8)
        ax_in.set_title('Fraction of {}'.format(ns))
    V = glob(path_in+'/*.V.stat')[0]
    D = glob(path_in+'/*.D.stat')[0]
    J = glob(path_in+'/*.J.stat')[0]
    list_tmp = ['V', 'D', 'J']
    name = re.split('\.', os.path.basename(V))[0]
    dir_s = os.path.dirname(V)
    i = 0
    for path in [V,D,J]:
        np_tmp = np.loadtxt(path, dtype='S10')
        PlotPie(np_tmp, axs[i], list_tmp[i])
        i += 1
    axs[-1].axis('off')
    fig.subplots_adjust(wspace=1)
    fig.suptitle('Usage of VDJ genes ({})'.format(xlb))
    plt.savefig(os.path.join(dir_s, 'FractionOfVDJOf{}.png'.format(xlb)), bbox_inches='tight')

def ReplaceLabel(array_in):
    dict_tmp = {}
    m = 0
    n = 0
    array_out = np.zeros(array_in.shape)
    for i in array_in:
        if i not in dict_tmp:
            dict_tmp[i] = m
            m += 1
            array_out[n] = dict_tmp[i]
        else:
            array_out[n] = dict_tmp[i]
        n += 1
    return array_out

def PlotVJComb(path_in, xlb):
    '''
    plot 3d-hist of VJ combination
    '''
    fig = plt.figure(figsize=(20, 10), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    VJ = glob(path_in+'/*.VJCom.stat')[0]
    name = re.split('\.', os.path.basename(VJ))[0]
    dir_s = os.path.dirname(VJ)
    np_tmp = np.loadtxt(VJ, dtype='S10')
    list_s = []
    ms = 0
    for ay in np_tmp:
        ms += 1
        if ay[0] not in list_s:
            list_s.append(ay[0])
        if len(list_s) == 30:
            break
    np_tmp = np_tmp[:ms,:]
    x = np_tmp[:,0]
    xpos = ReplaceLabel(x)
    y = np_tmp[:,1]
    ypos = ReplaceLabel(y)
    z = np.zeros(x.shape)
    dx = 0.5*np.ones_like(z)
    dy = dx.copy()
    dz = np_tmp[:,2].astype('int')
    col = get_cmap(len(set(list(ypos))))
    colors = np.array([col[i] for i in ypos.astype('int')])
    ax.bar3d(xpos, ypos, z, dx, dy, dz, color=colors, zsort='average',\
             alpha=0.5)
    ax.w_xaxis.set_ticks(xpos)
    ax.w_xaxis.set_ticklabels(x, rotation=20, va='center', ha='right', fontsize=6)
    ax.set_xlabel('V Gene')
    ax.w_yaxis.set_ticks(ypos)
    ax.w_yaxis.set_ticklabels(y)
    ax.set_ylabel('J Gene')
    ax.set_zlabel('Count')
    ax.xaxis.labelpad=15
    ax.yaxis.labelpad=15
    ax.zaxis.labelpad=15
    fig.suptitle('Distribution of VJ combination ({})'.format(xlb))
    plt.savefig(os.path.join(dir_s,\
                             'DistributionOfVJCombinationOf{}.png'.format(xlb)), bbox_inches='tight')

def CountBar(np_in):
    a,b,c,d,e,f,g,h = 0,0,0,0,0,0,0,0
    tl = len(np_in)
    for i in np_in:
        if i <= 5:
            a += 1
        elif 5<i<=10:
            b += 1
        elif 10<i<=30:
            c += 1
        elif 30<i<=50:
            d += 1
        elif 50<i<=100:
            e += 1
        elif 100<i<=1000:
            f += 1
        elif 1000<i<=10000:
            g += 1
        elif i>10000:
            h += 1
    np_c = np.array([int(round(m, 2)*100) for m in [float(n)/tl for n in\
                                          [a,b,c,d,e,f,g,h]]])
    return np.array(['0','<5','5-10','10-30','30-50','50-100',\
                     '100-1000','1000-10000', '>10000']),np_c


def PlotConst(path_in, xlb):
    path = glob(path_in+'/*_atleast-2_headers.tab')[0]
    fig, axes = plt.subplots()
    np_tmp = np.loadtxt(path, dtype='S10')
    np_in = np_tmp[1:, 1].astype('int')
    label, y = CountBar(np_in)
    axes.bar(range(1,9),y)
    axes.set_xlabel(xlb)
    axes.set_ylabel('Percentage(%)')
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.set_xticklabels(label, fontsize=7)
    axes.set_title('Distribution of CONSCOUNT')
    plt.savefig('DistributionOfCONSCOUNTOf{}.png'.format(xlb))

def main():
    if sys.argv[1] == 'PlotCDR3Bar':
        list_path = re.split(',', sys.argv[2])
        sample = sys.argv[3]
        PlotCDR3Bar(list_path, sample, sys.argv[4])
    elif sys.argv[1] == 'PlotVDJ':
        PlotVDJ(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'PlotVJComb':
        PlotVJComb(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'PlotConst':
        PlotConst(sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()

