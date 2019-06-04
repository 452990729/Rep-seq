#!/usr/bin/env python2


import os
import re
import sys
import numpy as np
import random
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def HandleSample(file_in, tp):
    list0 = []
    list1_3 = []
    list4_6 = []
    list7_9 = []
    list10_12 = []
    list13_15 = []
    list16 = []
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            try:
                if tp == 'N1':
                    num = int(re.split('\t', line)[18])
                elif tp == 'N2':
                    num = int(re.split('\t', line)[23])
                if num == 0:
                    list0.append(num)
                elif num >=1 and num <=3:
                    list1_3.append(num)
                elif num >=4 and num <=6:
                    list4_6.append(num)
                elif num >=7 and num <=9:
                    list7_9.append(num)
                elif num >=10 and num <=12:
                    list10_12.append(num)
                elif num >=13 and num <=15:
                    list13_15.append(num)
                elif num >=16:
                    list16.append(num)
            except ValueError:
                pass
    list_len = [len(list0), len(list1_3), len(list4_6), len(list7_9),\
                   len(list10_12), len(list13_15), len(list16)]
    list_std = [np.std(list0, ddof = 1), np.std(list1_3, ddof = 1),\
                    np.std(list4_6, ddof = 1), np.std(list7_9, ddof = 1),\
                   np.std(list10_12, ddof = 1), np.std(list13_15, ddof = 1),\
                   0.0]
    total = sum(list_len)
    return np.array([round(float(m)/total, 4)*100 for m in list_len]), np.array(list_std)

def GetData(inpath, list_group):
    dict_N1 = {}
    dict_N2 = {}
    for line in list_group:
        fl = os.path.join(inpath+'/'+line, line+\
                          '_R12_atleast-2_db-pass_FUNCTIONAL-T_clone-pass.tab')
        length_N1, std_N1 = HandleSample(fl, 'N1')
        length_N2, std_N2 = HandleSample(fl, 'N2')
        dict_N1[line] = (length_N1, std_N1)
        dict_N2[line] = (length_N2, std_N2)
    return dict_N1, dict_N2

def get_cmap(n, name='plasma'):
    cap = plt.cm.get_cmap(name, n+1)
    list_tmp = [cap(i) for i in range(n)]
#    random.shuffle(list_tmp)
    return list_tmp

def BarPlot(dict_in, list_group, outpath, tp):
    fig, ax = plt.subplots(figsize=(12,7))
    colors = get_cmap(len(list_group))
    ind = np.arange(len(dict_in[list_group[0]][0]))
    width = 0.8
    m = 0
    for key in list_group:
        if m < len(list_group)/2:
            rects = ax.bar(ind - (width/len(list_group))*(len(list_group)/2 - m-0.5),\
                          dict_in[key][0], width/len(list_group), yerr=dict_in[key][1],\
                          color=colors[m], label=key)
        else:
            rects = ax.bar(ind + (width/len(list_group))*(m+0.5-len(list_group)/2),\
                          dict_in[key][0], width/len(list_group), yerr=dict_in[key][1],\
                          color=colors[m], label=key)
        m += 1
    ax.set_xlabel('{} nucleotide addition [nt]'.format(tp))
    ax.set_ylabel('% of all unique sequences')
    ax.set_xticks(ind)
    ax.set_xticklabels(['0', '1-3', '4-6', '7-9', '10-12', '13-15', '16+'],\
                      rotation=45)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend()
    plt.savefig(outpath+'ComparisonOf{}Addition.pdf'.format(tp))
    plt.savefig(outpath+'ComparisonOf{}Addition.jpg'.format(tp), dpi=400)

def main():
    with open(sys.argv[2], 'r') as f:
        list_group = [i.strip() for i in f]
    dict_N1, dict_N2 = GetData(sys.argv[1], list_group)
    BarPlot(dict_N1, list_group, sys.argv[3], 'N1')
    BarPlot(dict_N2, list_group, sys.argv[3], 'N2')


if __name__ == '__main__':
    main()
