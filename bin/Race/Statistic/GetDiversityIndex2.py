#!/usr/bin/env python2


import sys
import re
import math
import os
from glob import glob

def GetD50(list_in):
    list_sort = sorted(list_in, reverse=True)
    total = sum(list_sort)
    m = 0
    n = 0
    for i in list_sort:
        m += i
        n += 1
        if m >= float(total)/2:
            D50 = round(float(n)/len(list_sort), 4)
            break
    return D50

def GetSimpson(list_in):
    total = sum(list_in)
    m = 0
    for i in list_in:
        sp = round(float(i)/total, 6)
        m += sp*sp
    Simpson = round(m, 4)
    return Simpson

def GetShannon(list_in):
    total = sum(list_in)
    m = 0
    for i in list_in:
        sp = round(float(i)/total, 8)
        m += sp*math.log(sp,math.e)
    Shannon = round(-m, 4)
    return Shannon

def GetRichness(list_in):
    return len(list_in)

def ReadTab(file_in):
    with open(file_in, 'r') as f:
        return [int(float(re.split('\t', line)[1])) for line in f.readlines()[1:]]


def main():
    out = open(sys.argv[1]+'/DiversityIndex.xls', 'w')
    out.write('\t'.join(['Sample', 'D50', 'Simpson', 'Shannon', 'Richness'])+'\n')
    files = glob(sys.argv[1]+'/*.CloneFilter.txt')
    for fl in files:
        list_sp = ReadTab(fl)
        D50 = GetD50(list_sp)
        Simpson = GetSimpson(list_sp)
        Shannon = GetShannon(list_sp)
        Richness = GetRichness(list_sp)
        lb = re.split('\.', os.path.basename(fl))[0]
        out.write('\t'.join([lb, str(D50), str(Simpson), str(Shannon), str(Richness)])+'\n')
    out.close()


if __name__ == '__main__':
    main()


