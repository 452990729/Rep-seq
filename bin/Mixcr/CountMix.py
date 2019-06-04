#!/usr/bin/env python2

import re
import sys
import os
from glob import glob
from copy import deepcopy
from collections import Counter

class Clone(object):
    def __init__(self, line_in):
        list_split = re.split('\t', line_in)
        self.cloneCount = list_split[1]
        self.cloneFraction = float(list_split[2])
        self.V = list_split[3]
        self.VJ = '|'.join([list_split[3], list_split[5]])
        self.VDJ = '|'.join([list_split[3], list_split[4], list_split[5]])
        self.aaCDR3 = list_split[-1]

    def UpdateVFraction(self, dict_in):
        self.VFraction = dict_in[self.V]

    def UpdateVJFraction(self, dict_in):
        self.VJFraction = dict_in[self.VJ]

    def UpdateVDJFraction(self, dict_in):
        self.VDJFraction = dict_in[self.VDJ]

def GetFraction(list_in, tp):
    total = len(list_in)
    if tp == 'V':
        dict_tmp = dict(Counter([ob.V for ob in list_in]))
        dict_re = {i:round(float(dict_tmp[i])/total, 4) for i in dict_tmp}
        for ob in list_in:
            ob.UpdateVFraction(dict_re)
    elif tp == 'VJ':
        dict_tmp = dict(Counter([ob.VJ for ob in list_in]))
        dict_re = {i:round(float(dict_tmp[i])/total, 4) for i in dict_tmp}
        for ob in list_in:
            ob.UpdateVJFraction(dict_re)
    elif tp == 'VDJ':
        dict_tmp = dict(Counter([ob.VDJ for ob in list_in]))
        dict_re = {i:round(float(dict_tmp[i])/total, 4) for i in dict_tmp}
        for ob in list_in:
            ob.UpdateVDJFraction(dict_re)

def HandleClone(file_in):
    '''
    Handle the MiXCR clone file -> dict[clonetype]=percentage
    '''
    list_ob = []
    with open(file_in, 'r') as f:
        for line in f.readlines()[1:]:
            list_ob.append(Clone(line.strip()))
    GetFraction(list_ob, 'V')
    GetFraction(list_ob, 'VJ')
    GetFraction(list_ob, 'VDJ')
    return list_ob

def GetOut(path_in, tp, OUT):
    list_sample = []
#    list_tmp = []
    set1 = set()
    for path in sorted(path_in):
        sample = re.split('\.', os.path.basename(path))[0]
        list_sample.append(str(sample))
        list_ob = HandleClone(path)
        if tp == 'V':
            locals()[sample] = {ob.V:ob.VFraction for ob in list_ob}
        elif tp == 'VJ':
            locals()[sample] = {ob.VJ:ob.VJFraction for ob in list_ob}
        elif tp == 'VDJ':
            locals()[sample] = {ob.VDJ:ob.VDJFraction for ob in list_ob}
        elif tp == 'Clonetype':
            locals()[sample] = {ob.aaCDR3:ob.cloneFraction for ob in list_ob}
#        for key in locals()[sample]:
#            if key not in list_tmp:
#                list_tmp.append(key)
        set1 = set1 | set(locals()[sample].keys())
    dict_tmp = deepcopy(locals()[list_sample[0]])
    for key in set1:
        if key not in dict_tmp:
            dict_tmp[key] = 0
        else:
            dict_tmp[key] = float(dict_tmp[key])
    list_tmp = sorted(list(set1), key=lambda x:dict_tmp[x] ,reverse=True)
    for key in list_tmp:
        list_out = [key,]
        for sample in list_sample:
            if key not in locals()[sample]:
                list_out.append(str(0))
            else:
                list_out.append(str(locals()[sample][key]))
        OUT.write('\t'.join(list_out)+'\n')
    OUT.close()

def main():
    paths = glob(sys.argv[1]+'/*/*/out/*.CloneFilter.txt')
    out1 = open(os.path.join(sys.argv[2], 'ClonetypeFraction.txt'), 'w+')
    out2 = open(os.path.join(sys.argv[2], 'VFraction.txt'), 'w+')
    out3 = open(os.path.join(sys.argv[2], 'VJFraction.txt'), 'w+')
    out4 = open(os.path.join(sys.argv[2], 'VDJFraction.txt'), 'w+')
    list_sample = []
    for path in paths:
        list_sample.append(re.split('\.', os.path.basename(path))[0])
    out1.write('\t'.join(['Clonetype', ]+list_sample)+'\n')
    GetOut(paths, 'Clonetype', out1)
    out2.write('\t'.join(['VGene', ]+list_sample)+'\n')
    GetOut(paths, 'V', out2)
    out3.write('\t'.join(['VJGene', ]+list_sample)+'\n')
    GetOut(paths, 'VJ', out3)
    out4.write('\t'.join(['VDJGene', ]+list_sample)+'\n')
    GetOut(paths, 'VDJ', out4)


if __name__ == '__main__':
    main()
