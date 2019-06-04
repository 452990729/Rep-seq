#!/usr/bin/env python

import re
#import numpy as np
from collections import Counter
from itertools import product
#from Bio import SeqIO


def NW(seq1, seq2):
    '''
    the Needleman/Wunsch log
    return the LCS(seq1, seq2)
    '''
    shape = (len(seq1)+1, len(seq2)+1)
    np_NW = np.zeros(shape, dtype='int16')
    l1 = len(seq1)
    l2 = len(seq2)
    for i in range(l1):
        for j in range(l2):
            if seq1[i] == seq2[j]:
                np_NW[i+1,j+1] = np_NW[i,j] + 1
            else:
                np_NW[i+1,j+1] = max(np_NW[i+1,j], np_NW[i,j+1])
    return l1 - np_NW[-1,-1]

def Dist(umi1, umi2, max = float("inf")):
    result = 1
    for i in range(min(len(umi1), len(umi2))):
        result += 1 if umi1[i] != umi2[i] else 0
        if result > max+1:
            return False
    return result

def MafDist(s1, s2, n):
    '''
    has at most n differences, or exactly one deletion
    '''
    if s1 == s2:
        return True
    if len(s1) != len(s2):
        return False
    errors = 0
    for i in range(len(s1)):
        if (s1[i] != s2[i]):
            errors += 1
            if s1[i+1:] == s2[i+1:]:
                return True
            if errors == n:
                return False
    assert False, "Bug in the code. please report"

def HandleFastq(file_in):
    '''
    return a list of UMI
    '''
    i = 0
    list_tmp = []
    with open(file_in, 'r') as in1:
        for line in in1:
            i += 1
            if i%4 == 0:
                list_tmp.append(line.strip())
    return [i for i in set(list_tmp)]

def HandleFasta(file_in):
    '''
    return a list of UMI
    '''
    list_tmp = [str(i.seq) for i in SeqIO.parse(file_in, 'fasta')]
    return dict(Counter(list_tmp))

class Fastq(object):
    '''
    analyse the fastq format
    '''
    def __init__(self, list_in):
        list_split = re.split('\s+', list_in[0])
        self.id = re.sub('@', '', list_split[0])
        list_bar = re.split('\+', re.split('\:', list_split[1])[-1])
        self.barcode = list_bar[0]
        self.index = list_bar[1]
        self.seq = list_in[1]
        self.third = list_in[2]
        self.quality = list_in[3]
        self.raw = '\n'.join(list_in)

    def MakeFs(self, barcode):
        '''
        return the format fastq
        '''
        seq_id = '@'+self.id+' '+'INDEX='+self.index+'|BARCODE='+barcode
        return '\n'.join([seq_id, self.seq, self.third, self.quality])

def Json2Str(input):
    if isinstance(input, dict):
        return {Json2Str(key): Json2Str(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [Json2Str(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class Tab(object):
    '''
    handle the umi-chango output tab file
    '''
    def __init__(self, line_in):
        list_split = re.split('\t', line_in)
        self.SEQUENCE_ID = list_split[0]
        self.SEQUENCE_INPUT = list_split[1]
        self.V_CALL = list_split[7]
        self.D_CALL = list_split[8]
        self.J_CALL = list_split[9]
        self.CDR3_IMGT = list_split[-12]
        self.CONSCOUNT = int(list_split[-3])
        self.DUPCOUNT = int(list_split[-2])
        self.CLONE = int(list_split[-1])
        self.VJCombination = re.split('\*', re.split(',', self.V_CALL)[0])[0]\
                +','+re.split('\*', re.split(',', self.J_CALL)[0])[0]

class Tab2(object):
    '''
    handle the NOUMI changeo output tab
    '''
    def __init__(self, line_in):
        list_split = re.split('\t', line_in)
        self.SEQUENCE_ID = list_split[0]
        self.SEQUENCE_INPUT = list_split[1]
        self.V_CALL = list_split[7]
        self.D_CALL = list_split[8]
        self.J_CALL = list_split[9]
        self.CDR3_IMGT = list_split[-11]
        self.DUPCOUNT = int(list_split[-2])
        self.CLONE = int(list_split[-1])
        self.VJCombination = re.split('\*', re.split(',', self.V_CALL)[0])[0]\
                +','+re.split('\*', re.split(',', self.J_CALL)[0])[0]

def ReadChangoTab(file_in, type_in='umi'):
    '''
    read the ReadChangoTab -> list(ob(Tab))
    '''
    with open(file_in, 'r') as in1:
        if type_in == 'umi':
            return [Tab(i.strip()) for i in in1.readlines()[1:]]
        elif type_in == 'noumi':
            return [Tab2(i.strip()) for i in in1.readlines()[1:]]


def HandleDegenerateBase(seq_in):
    '''
    handle the Degenerate Base
    return a list
    '''
    dict_db = {'R':['A', 'G'], 'Y':['C', 'T'],\
               'M':['A', 'C'], 'K':['G', 'T'],\
               'S':['G', 'C'], 'W':['A', 'T'],\
               'H':['A', 'T', 'C'], 'B':['G', 'T', 'C'],\
               'V':['G', 'A', 'C'], 'D':['G', 'A', 'T'],\
               'N':['A', 'T', 'C', 'G']}
    set_b = set(['A', 'T', 'C', 'G'])
    list_p = []
    list_b = []
    list_re = []
    m = 0
    for i in seq_in:
        if i not in set_b:
            list_p.append(m)
            list_b.append(i)
        m += 1
    if len(list_b) == 0:
        return [seq_in]
    list_base = list(product(*[dict_db[i] for i in list_b]))
    list_seq = list(seq_in)
    for tp in list_base:
        for ct, bp in enumerate(tp):
            list_seq[list_p[ct]] = bp
        list_re.append(''.join(list_seq))
    return list_re



