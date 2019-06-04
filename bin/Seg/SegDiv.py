#!/usr/bin/env python

import sys
import re
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from copy import deepcopy
from workflow import Dist

def ReadFastq(file_in):
    i = 0
    list_tmp = []
    with open(file_in, 'r') as in1:
        for line in in1:
            i += 1
            if i%4 == 2:
                list_tmp.append(line.strip())
    return list_tmp

def HandleUMI(set_UMI, mismatch):
    set1 = set()
    set2 = set()
    total = len(set_UMI)
    set_copy = deepcopy(set_UMI)
    for ref in set_UMI:
        if ref not in set1:
            list_group = [ref]
            set1.add(ref)
            set_copy.remove(ref)
            for qy in set_copy.copy():
                if Dist(ref, qy, mismatch):
                    list_group.append(qy)
                    set1.add(qy)
                    set_copy.remove(qy)
            set2.add(tuple(list_group))
    return float(len(set2))

def Process(list_umi):
    proi = HandleUMI(set(list_umi), 2)
    proi_int = int(proi)
    np_pet = np.zeros(50)
    t1= HandleUMI(set(list_umi[:proi_int]), 2)
    np_pet[0] = round((t1/proi)*100, 2)
    for i in range(2,51):
        print i
        list_in = list_umi[:(i-1)*5*proi_int]
        t1 = HandleUMI(set(list_in), 2)
        np_pet[i-1] = round((t1/proi)*100, 2)
        i += 1
    return np_pet

def Plot(np_in):
    fig, ax = plt.subplots()
    ax.plot(np.arange(1, 51), np_in)
    ax.set_xticklabels([0 , 0, 40, 80, 120, 160, 200])
    ax.set_xlabel('Sequencing Depth')
    ax.set_ylabel('UMI Saturation(%)')
    ax.set_title('UMI Saturation VS Sequencing Depth')
    fig.savefig('test1.png')


def main():
    list_umi = ReadFastq(sys.argv[1])
    print 'end of creating dict_umi'
    np_pet = Process(list_umi)
    Plot(np_pet)
if __name__ == '__main__':
    main()

