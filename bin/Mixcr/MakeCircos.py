#!/usr/bin/env python2

import sys
import re
import os
from Alignment import NW

class Clone(object):
    def __init__(self, line_in, label):
        list_tmp = re.split('\t', line_in)
        self.clone = list_tmp[0]
        self.V = list_tmp[3]
        self.J = list_tmp[5]
        self.CDR3 = list_tmp[-1]
        self.nucl = list_tmp[-2]
        self.label = label
        self.line = line_in
        self.count = int(list_tmp[1])
#        self.start = 0
#        self.end = 0

    def UpdateLen(self, start):
        self.start = start
        self.end = self.start+self.count

def ReadClone(file_in):
    list_tmp = []
    base = re.split('\.', os.path.basename(file_in))[0]
    start = 0
    with open(file_in, 'r') as f:
        for line in f.readlines()[::-1][:-1]:
            ob = Clone(line.strip(), base)
            ob.UpdateLen(start+1)
            start = ob.end
            list_tmp.append(ob)

    return list_tmp
#    return {i.CDR3:i for i in list_tmp}

def main():
    list1 = ReadClone(sys.argv[1])
    list2 = ReadClone(sys.argv[2])
    out = open('1.0nucllinks.conf', 'w+')
    out2 = open('1.0NuclSimilarity.txt', 'w+')
    out2.write('Col'+'\t'+'V'+'\t'+'J'+'\t'+'PB7'+'\t'+'SB7'+'\t'+'similarity'+'\n')
#    out2 = open('2.list', 'w+')
#    out12 = open('12.list', 'w+')
#    out21 = open('21.list', 'w+')
    i = 0
    for ob1 in list1:
        for ob2 in list2:
            if ob1.V == ob2.V and ob1.J == ob2.J:
                com = NW(ob1.nucl, ob2.nucl)
                a = round(float(com)/len(ob1.nucl), 2)
                b = round(float(com)/len(ob2.nucl), 2)
#                if a >=0.85 and b >=0.85:
                if ob1.nucl == ob2.nucl:
                    i += 1
                    out.write('\t'.join([str(i), ob1.label, \
                               str(ob1.start), str(ob1.end)])+'\n')
                    out.write('\t'.join([str(i), ob2.label, \
                               str(ob2.start), str(ob2.end)])+'\n')
                    out2.write('\t'.join([str(i), ob1.V, ob1.J, ob1.nucl,\
                                          ob2.nucl, str(min(a,b))])+'\n')
                    out.flush()
    out.close()
    out2.close()
#    set_tmp = set(dict1.keys())&set(dict2.keys())
#    for key in dict1:
#        if key in set_tmp:
#            out12.write(dict1[key].line+'\n')
#        else:
#            out1.write(dict1[key].line+'\n')
#    for key in dict2:
#        if key in set_tmp:
#            out21.write(dict2[key].line+'\n')
#        else:
#            out2.write(dict2[key].line+'\n')
#    out1.close()
#    out2.close()
#    out12.close()
#    out21.close()


if __name__ ==  '__main__':
    main()
