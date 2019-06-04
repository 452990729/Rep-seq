#!/usr/bin/env python


import sys
import os
import re
from collections import Counter


class Tab(object):
    def __init__(self, line):
        list_split = re.split('\t', line.strip())
        self.cloneId = list_split[0]
        self.cloneCount = int(list_split[-2])
        self.clonetype = int(list_split[-1])
        self.bestVGene = re.split('\*', re.split(',', list_split[7])[0])[0]
        self.bestDGene = re.split('\*', re.split(',', list_split[8])[0])[0]
        self.bestJGene = re.split('\*', re.split(',', list_split[9])[0])[0]
        self.bestVFamily = re.split('\-', re.split('\/', self.bestVGene)[0])[0]
        self.bestDFamily = re.split('\-', re.split('\/', self.bestDGene)[0])[0]
        self.bestJFamily = re.split('\-', re.split('\/', self.bestJGene)[0])[0]
        self.nSeqCDR3 = list_split[-5]
        self.aaSeqCDR3 = list_split[-4]
        self.VJ = ','.join([self.bestVGene, self.bestJGene])
        self.VDJ = ','.join([self.bestVGene, self.bestDGene, self.bestJGene])
        self.fraction = 0

    def UpdateCloneCount(self, num):
        self.cloneCount += num

    def UpdateFraction(self, total):
        self.fraction = round(float(self.cloneCount)/total, 20)

    def WriteFn(self, fn):
        fn.write('\t'.join([str(self.clonetype), str(self.cloneCount), str(self.fraction),\
                           self.bestVGene, self.bestDGene, self.bestJGene,\
                           self.bestVFamily, self.bestDFamily, self.bestJFamily,\
                           self.VJ, self.VDJ, self.nSeqCDR3,\
                            self.aaSeqCDR3])+'\n')

def ReadTab(file_in, name, pathout):
    dict_tmp = {}
    total = 0
    with open(file_in, 'r') as in1:
        for line in in1.readlines()[1:]:
            ob = Tab(line)
            if ob.bestDGene:
                if ob.clonetype not in dict_tmp:
                    dict_tmp[ob.clonetype] = ob
                else:
                    dict_tmp[ob.clonetype].UpdateCloneCount(ob.cloneCount)
                total += ob.cloneCount
    out = open(os.path.join(pathout, name+'.clonetype.filter.txt'), 'w+')
    out.write('\t'.join(['clonetype', 'cloneCount', 'cloneFraction',\
                         'bestVGene', 'bestDGene', 'bestJGene','bestVFamily',\
                        'bestDFamily', 'bestJFamily', 'VJCombination',\
                         'VDJCombination', 'nSeqCDR3', 'aaSeqCDR3'])+'\n')
    for key in sorted(dict_tmp.keys()):
        dict_tmp[key].UpdateFraction(total)
        dict_tmp[key].WriteFn(out)
    out.close()
    return dict_tmp.values()

def StatCDR3Length(list_in, name, pathout):
    '''
    write out the stat of CDR3 length
    '''
    list_nCDR3Length = reduce(lambda x,y:x+y, [[len(i.nSeqCDR3)]*i.cloneCount for i in list_in])
    out1 = open(os.path.join(pathout, name+'.nCDR3.len.stat'), 'w+')
    for line in list_nCDR3Length:
        out1.write(name+'\t'+str(line)+'\n')
    out1.close()
    list_aCDR3Length = reduce(lambda x,y:x+y, [[len(i.aaSeqCDR3)]*i.cloneCount for i in list_in])
    out2 = open(os.path.join(pathout, name+'.aCDR3.len.stat'), 'w+')
    for line in list_aCDR3Length:
        out2.write(name+'\t'+str(line)+'\n')
    out2.close()

def VDJUsage(list_in, name, ts, pathout):
    '''
    stat the VDJ usage
    '''
    tl = sum([i.cloneCount for i in list_in])
    if ts == 'V':
        list_tmp = reduce(lambda x,y:x+y, [[i.bestVGene]*i.cloneCount for i in list_in])
    elif ts == 'D':
        list_tmp = reduce(lambda x,y:x+y, [[i.bestDGene]*i.cloneCount for i in list_in])
    elif ts == 'J':
        list_tmp = reduce(lambda x,y:x+y, [[i.bestJGene]*i.cloneCount for i in list_in])
    elif ts == 'VFamily':
        list_tmp = reduce(lambda x,y:x+y, [[i.bestVFamily]*i.cloneCount for i in list_in])
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
    tl = sum([i.cloneCount for i in list_in])
    list_tmp = reduce(lambda x,y:x+y, [[i.VJ]*i.cloneCount for i in list_in])
    out = open(os.path.join(pathout, '.'.join([name, 'VJCom.stat'])), 'w+')
    list_s = sorted(dict(Counter(list_tmp)).items(),\
            key=lambda x:x[1], reverse=True)
    for key,value in list_s:
        out.write('\t'.join(re.split(',', key))+'\t'+str(value)+'\t'+\
                  str(round((float(value)/tl)*100, 4))+'\n')
    out.close()

def VDJcomb(list_in, name, pathout):
    tl = sum([i.cloneCount for i in list_in])
    list_tmp = reduce(lambda x,y:x+y, [[i.VDJ]*i.cloneCount for i in list_in])
    out = open(os.path.join(pathout, '.'.join([name, 'VDJCom.stat'])), 'w+')
    list_s = sorted(dict(Counter(list_tmp)).items(),\
                    key=lambda x:x[1], reverse=True)
    for key,value in list_s:
        out.write('\t'.join(re.split(',', key))+'\t'+str(value)+'\t'+\
                  str(round((float(value)/tl)*100, 4))+'\n')
    out.close()

def main():
    list_ob = ReadTab(sys.argv[1], sys.argv[2], sys.argv[3])
#    os.mkdir('stats')
#    os.chdir('stats')
    StatCDR3Length(list_ob, sys.argv[2], sys.argv[3])
    VDJUsage(list_ob, sys.argv[2], 'V', sys.argv[3])
    VDJUsage(list_ob, sys.argv[2], 'D', sys.argv[3])
    VDJUsage(list_ob, sys.argv[2], 'J', sys.argv[3])
    VDJUsage(list_ob, sys.argv[2], 'VFamily', sys.argv[3])
    VJcomb(list_ob, sys.argv[2], sys.argv[3])
    VDJcomb(list_ob, sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()
