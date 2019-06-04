#!/usr/bin/env python2

import sys
import os
import re
from Bio.Seq import Seq
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle


def IsSilence(seq, tp):
    before, position, after = tp[0], int(tp[1:-1]), tp[-1]
    if position%3 == 0:
        a = seq[position-3:position-1]+before
        b = seq[position-3:position-1]+after
        p = position/3
    elif position%3 == 1:
        a = before+seq[position:position+2]
        b = after+seq[position:position+2]
        p = position/3 + 1
    elif position%3 == 2:
        a = seq[position-2]+before+seq[position]
        b = seq[position-2]+after+seq[position]
        p = position/3 + 1
    if str(Seq(a).translate()) == str(Seq(b).translate()):
        return 1,0,p
    else:
        return 0,1,p

def GetMutation(line_in):
    line = re.split('\|', line_in)[5]
    list_tmp = re.findall('S([^S^D^I]+)', line)
    return [i for i in list_tmp if int(i[1:-1])<=285]

def MakeArray(file_in):
    dict_tmp = {}
    tl = 0
    for i in range(95):
        dict_tmp[i+1] = [0, 0]
    with open(file_in, 'r') as in1:
        for line in in1:
            tl += 1
            list_split = re.split('\t', line.strip())
            list_m = GetMutation(list_split[2])
            seq = list_split[1]
            for m in list_m:
                s,r,p = IsSilence(seq, m)
                tp_tmp = [s,r]
                dict_tmp[p] = [dict_tmp[p][i]+tp_tmp[i] for i in\
                                   range(len(tp_tmp))]
    x = sorted(dict_tmp.keys())
    p1 = 0
    p2 = 0
    for value in dict_tmp.values():
        p1 += value[0]
        p2 += value[1]
    ratio = round(float(p2)/p1, 1)
    y1 = []
    y2 = []
    for i in x:
        y1.append(round(float(dict_tmp[i][0])*100/tl, 2))
        y2.append(round(float(dict_tmp[i][1])*100/tl, 2))
    return np.array(x), np.array(y1), np.array(y2), ratio

def MakePlot(x, y1, y2, ratio, lb, sample):
    fig, axe = plt.subplots(figsize=(60,30))
    width = 1
    st = \
    'EVQLQQSGPELVKPGASVKISCKASGYTFTDYYMNWVKQSHGKSLEWIGDINPNNGGTSYNQKFKGKATLTVDKSSSTAYMELRSLTSEDSAVYY'
#   IGHV1-26:
#   EVQLQQSGPELVKPGASVKISCKASGYTFTDYYMNWVKQSHGKSLEWIGDINPNNGGTSYNQKFKGKATLTVDKSSSTAYMELRSLTSEDSAVYY
#   IGHV1-64:
#    QVQLQQPGAELVKPGASVKLSCKASGYTFTSYWMHWVKQRPGQGLEWIGMIHPNSGSTNYNEKFKSKATLTVDKSSSTAYMQLSSLTSEDSAVYY
    p1 = axe.bar(x, y1, width, color='#d62728')
    p2 = axe.bar(x, y2, width, bottom=y1)
    extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none',\
                      linewidth=0)
    axe.set_xlabel(lb, fontsize=40)
    axe.set_ylabel('Frequency of mutations(%)', fontsize=40)
    axe.legend((p2[0], p1[0], extra),('Replacement', 'Silent',\
                                      'ratio={}'.format(str(ratio))), fontsize=30)
    axe.set_xticks(x)
    axe.set_xticklabels([i for i in st], fontsize=30)
    for label in axe.get_yticklabels():
        label.set_fontsize(30)
    plt.savefig('{}.{}.png'.format(sample, lb), dpi=100)

def main():
    x, y1, y2, ratio = MakeArray(sys.argv[1])
    list_tmp = re.split('\.', os.path.basename(sys.argv[1]))
    sample = list_tmp[0]
    lb = list_tmp[1]
    MakePlot(x, y1, y2, ratio, lb, sample)


if __name__ == '__main__':
    main()


