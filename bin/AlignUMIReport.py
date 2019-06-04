#!/usr/bin/env python

import sys
import re
import json
from copy import deepcopy
from workflow import Dist

def ReadFastq(file_in):
    i = 0
    dict_tmp = {}
    with open(file_in, 'r') as in1:
        for line in in1:
            i += 1
            if i == 1:
                ids = re.split('\s+', line.strip())[0]
            if i == 2:
                seq = line.strip()
                if seq not in dict_tmp:
                    dict_tmp[seq] = [ids]
                else:
                    dict_tmp[seq] += [ids]
            elif i == 4:
                i = 0
    return dict_tmp

def HandleUMI(set_UMI, mismatch):
    set1 = set()
    set2 = set()
    print 'number of umis   '+str(len(set_UMI))
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
    print 'number of corrected uims '+str(len(set2))
    print float(len(set2))/len(set_UMI)
    return set2

def MakeJson(set_in, dict_in, json_out):
    dict_tmp = {}
    out = open(json_out, 'w+')
    for tp in set_in:
        seed = tp[0]
        for rf in tp:
            for rs in dict_in[rf]:
                dict_tmp[rs] = seed
    out.write(json.dumps(dict_tmp))
    out.close()

def main():
    dict_umi = ReadFastq(sys.argv[1])
    print 'end of creating dict_umi'
    set2 = HandleUMI(set(dict_umi.keys()), 1)
    print 'end of grouping umi'
#    MakeJson(set2, dict_umi, sys.argv[2])

if __name__ == '__main__':
    main()

