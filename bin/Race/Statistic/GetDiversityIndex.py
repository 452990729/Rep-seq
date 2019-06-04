#!/usr/bin/env python2


import sys
import re
import math
import os


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
        sp = round(float(i)/total, 6)
        m += sp*math.log(sp,math.e)
    Shannon = round(-m, 4)
    return Shannon

def GetRichness(list_in):
    return len(list_in)

def ReadTab(file_in):
    with open(file_in, 'r') as f:
        return [int(re.split('\t', line)[1]) for line in f.readlines()[1:]]


def main():
    out = open(sys.argv[1]+'/Compare/DiversityIndex.xls', 'w')
    out.write('\t'.join(['Group', 'Sample', 'D50', 'Simpson', 'Shannon', 'Richness'])+'\n')
    root, dirs, files = next(os.walk(sys.argv[1]+'/analysis'))
    for dr in sorted(dirs):
        root2, dirs2, files2 = next(os.walk(os.path.join(root, dr)))
        for d in dirs2:
            fl = root+'/'+dr+'/'+d+'/5.stats/'+d+'.clonetype.filter.txt'
            list_sp = ReadTab(fl)
            D50 = GetD50(list_sp)
            Simpson = GetSimpson(list_sp)
            Shannon = GetShannon(list_sp)
            Richness = GetRichness(list_sp)
            out.write('\t'.join([dr, d, str(D50), str(Simpson), str(Shannon), str(Richness)])+'\n')
    out.close()


if __name__ == '__main__':
    main()


