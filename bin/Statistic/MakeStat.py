#!/usr/bin/env python


import sys
import os
import re
from collections import Counter
from workflow import ReadChangoTab


def StatCDR3Length(list_in, name):
    '''
    write out the stat of CDR3 length
    '''
    list_CDR3Length = [len(i.CDR3_IMGT) for i in list_in]
    out = open(name+'.CDR3.len.stat', 'w+')
    for line in list_CDR3Length:
        out.write(name+'\t'+str(line)+'\n')
    out.close()

def VDJUsage(list_in, name, ts):
    '''
    stat the VDJ usage
    '''
    if ts == 'V':
        list_tmp = [re.split('\*', re.split(',', i.V_CALL)[0])[0] \
                for i in list_in]
    elif ts == 'D':
        list_tmp = [re.split('\*', re.split(',', i.D_CALL)[0])[0] \
                for i in list_in]
    elif ts == 'J':
        list_tmp = [re.split('\*', re.split(',', i.J_CALL)[0])[0] \
                for i in list_in]
    out = open('.'.join([name, ts, 'stat']), 'w+')
    list_s = sorted(dict(Counter(list_tmp)).items(),\
            key=lambda x:x[1], reverse=True)
    for key,value in list_s:
        if not key:
            out.write('OTHER'+'\t'+str(value)+'\n')
        else:
            out.write(key+'\t'+str(value)+'\n')
    out.close()

def VJcomb(list_in, name):
    '''
    stat of the VJCombination
    '''
    list_tmp = [i.VJCombination for i in list_in]
    out = open('.'.join([name, 'VJCom.stat']), 'w+')
    list_s = sorted(dict(Counter(list_tmp)).items(),\
            key=lambda x:x[1], reverse=True)
    for key,value in list_s:
        out.write('\t'.join(re.split(',', key))+'\t'+str(value)+'\n')
    out.close()

def CloneNoUMIStat(list_in, name):
    dict_read = {}
    dict_uniq = {}
    for ob in list_in:
        if ob.CLONE not in dict_read:
            dict_read[ob.CLONE] = ob.DUPCOUNT
            dict_uniq[ob.CLONE] = 1
        else:
            dict_read[ob.CLONE] += ob.DUPCOUNT
            dict_uniq[ob.CLONE] += 1
    out = open('.'.join([name, 'Clone.stat']), 'w+')
    for key in sorted(dict_uniq.keys()):
        out.write('\t'.join([name, str(key), str(dict_uniq[key]),\
                             str(dict_read[key])])+'\n')
    out.close()

def CloneStat(list_in, name):
    dict_read = {}
    dict_uniq = {}
    for ob in list_in:
        if ob.CLONE not in dict_read:
            dict_read[ob.CLONE] = ob.CONSCOUNT
            dict_uniq[ob.CLONE] = ob.DUPCOUNT
        else:
            dict_read[ob.CLONE] += ob.CONSCOUNT
            dict_uniq[ob.CLONE] += ob.DUPCOUNT
    out = open('.'.join([name, 'Clone.stat']), 'w+')
    for key in sorted(dict_uniq.keys()):
        out.write('\t'.join([name, str(key), str(dict_uniq[key]),\
                             str(dict_read[key])])+'\n')
    out.close()

def main():
    list_ob = ReadChangoTab(sys.argv[1], sys.argv[3])
    os.mkdir('stats')
    os.chdir('stats')
    StatCDR3Length(list_ob, sys.argv[2])
    VDJUsage(list_ob, sys.argv[2], 'V')
    VDJUsage(list_ob, sys.argv[2], 'D')
    VDJUsage(list_ob, sys.argv[2], 'J')
    VJcomb(list_ob, sys.argv[2])
    if sys.argv[3] == 'umi':
        CloneStat(list_ob, sys.argv[2])
    elif sys.argv[3] == 'noumi':
        CloneNoUMIStat(list_ob, sys.argv[2])


if __name__ == '__main__':
    main()
