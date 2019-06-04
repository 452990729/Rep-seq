#!/usr/bin/env python


import sys
import os
import re
from collections import Counter

class Tab(object):
    def __init__(self, line):
        list_split = re.split('\t', line.strip())
        self.cloneId = list_split[0]
        self.cloneCount = list_split[1]
        self.bestVGene = list_split[3]
        self.bestDGene = list_split[4]
        self.bestJGene = list_split[5]
        self.nSeqCDR3 = list_split[-2]
        self.aaSeqCDR3 = list_split[-1]
        self.VJ = ','.join([self.bestVGene, self.bestJGene])
        self.VDJ = ','.join([self.bestVGene, self.bestDGene, self.bestJGene])

def ReadTab(file_in):
    list_tmp = []
    with open(file_in, 'r') as in1:
        for line in in1.readlines()[1:]:
            list_tmp.append(Tab(line))
    return list_tmp

def StatCDR3Length(list_in, name, pathout):
    '''
    write out the stat of CDR3 length
    '''
    list_nCDR3Length = [len(i.nSeqCDR3) for i in list_in]
    out1 = open(os.path.join(pathout, name+'.nCDR3.len.stat'), 'w+')
    for line in list_nCDR3Length:
        out1.write(name+'\t'+str(line)+'\n')
    out1.close()
    list_aCDR3Length = [len(i.aaSeqCDR3) for i in list_in]
    out2 = open(os.path.join(pathout, name+'.aCDR3.len.stat'), 'w+')
    for line in list_aCDR3Length:
        out2.write(name+'\t'+str(line)+'\n')
    out2.close()

def VDJUsage(list_in, name, ts, pathout):
    '''
    stat the VDJ usage
    '''
    tl = len(list_in)
    if ts == 'V':
        list_tmp = [i.bestVGene for i in list_in]
    elif ts == 'D':
        list_tmp = [i.bestDGene for i in list_in]
    elif ts == 'J':
        list_tmp = [i.bestJGene for i in list_in]
    out = open(os.path.join(pathout, '.'.join([name, ts, 'stat'])), 'w+')
    list_s = sorted(dict(Counter(list_tmp)).items(),\
            key=lambda x:x[1], reverse=True)
    for key,value in list_s:
        if not key:
            out.write('None'+'\t'+str(value)+'\t'+\
                      str(round((float(value)/tl)*100, 4))+'\n')
        else:
            out.write(key+'\t'+str(value)+'\t'+\
                      str(round((float(value)/tl)*100, 4))+'\n')
    out.close()

def VJcomb(list_in, name, pathout):
    '''
    stat of the VJCombination
    '''
    tl = len(list_in)
    list_tmp = [i.VJ for i in list_in]
    out = open(os.path.join(pathout, '.'.join([name, 'VJCom.stat'])), 'w+')
    list_s = sorted(dict(Counter(list_tmp)).items(),\
            key=lambda x:x[1], reverse=True)
    for key,value in list_s:
        out.write('\t'.join(re.split(',', key))+'\t'+str(value)+'\t'+\
                  str(round((float(value)/tl)*100, 4))+'\n')
    out.close()

def VDJcomb(list_in, name, pathout):
    tl = len(list_in)
    list_tmp = [i.VDJ for i in list_in]
    out = open(os.path.join(pathout, '.'.join([name, 'VDJCom.stat'])), 'w+')
    list_s = sorted(dict(Counter(list_tmp)).items(),\
                    key=lambda x:x[1], reverse=True)
    for key,value in list_s:
        out.write('\t'.join(re.split(',', key))+'\t'+str(value)+'\t'+\
                  str(round((float(value)/tl)*100, 4))+'\n')
    out.close()

def main():
    list_ob = ReadTab(sys.argv[1])
#    os.mkdir('stats')
#    os.chdir('stats')
    StatCDR3Length(list_ob, sys.argv[2], sys.argv[3])
    VDJUsage(list_ob, sys.argv[2], 'V', sys.argv[3])
    VDJUsage(list_ob, sys.argv[2], 'D', sys.argv[3])
    VDJUsage(list_ob, sys.argv[2], 'J', sys.argv[3])
    VJcomb(list_ob, sys.argv[2], sys.argv[3])
    VDJcomb(list_ob, sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()
