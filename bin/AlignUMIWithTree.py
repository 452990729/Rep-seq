#!/usr/bin/env python

import sys
import re
import json
from copy import deepcopy
from workflow import Dist

UMIS =[]
dict_umi = {}
dict_umi_count = {}
dict_gp = {}

class Tree(object):
    '''
    the node tree based on the umi similarity
    1 mismatch
    '''
    global UMIS, dict_umi

    def __init__(self, seq_in, mother):
#        global UMIS
        self.root = seq_in
        self.leaf = []
        self.tree = []
        self.mother = mother
        self.group = ''

    def GetLeaf(self):
        '''
        get the leaf of root
        '''
#        global UMIS
        for umi in UMIS:
            if Dist(self.root, umi, 1):
                self.leaf.append(umi)
                UMIS.remove(umi)
        if len(self.leaf) != 0:
            return True
    
    def CoseLeaf(self):
#        global dict_umi
        if self.GetLeaf():
            for umi in self.leaf:
                tree = Tree(umi, self.root)
                dict_umi[umi] = tree
                self.tree.append(tree)
                tree.CoseLeaf()
    
    def IsEnd(self):
        if not self.leaf:
            return True

    def IsContact(self, dict_in):
        if self.mother and dict_in[self.mother] >= dict_in[self.root]*2 -1:
            return True
    
    def UpdateGroup(self, name):
        self.group = name


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

def CutTree(tree_in):
    '''
    cut the tree
    '''
    global dict_umi
    global dict_gp
    global dict_umi_count
    if tree_in.mother:
        if tree_in.IsContact(dict_umi_count):
            tree_in.UpdateGroup(dict_umi[tree_in.mother].group)
            dict_gp[tree_in.group].append(tree_in.root)
        else:
            tree_in.UpdateGroup(tree_in.root)
            dict_gp[tree_in.group] = [tree_in.group]
    else:
        tree_in.UpdateGroup(tree_in.root)
        dict_gp[tree_in.group] = [tree_in.group]
    if not tree_in.IsEnd():
        for tree in tree_in.tree:
            CutTree(tree)

def HandleUMI(dict_in, js):
    global UMIS, dict_umi, dict_umi_count, dict_gp
    dict_umi_count = {key:len(dict_in[key]) for key in dict_in}
    UMIS = list(set(dict_umi_count.keys()))
    while 1:
        if UMIS:
            umi = sorted(UMIS, key=lambda x:dict_umi_count[x], reverse=True)[0]
            dict_gp[umi] = [umi]
            UMIS.remove(umi)
            tree = Tree(umi, 0)
            dict_umi[umi] = tree
            tree.CoseLeaf()
            CutTree(tree)
#            print 'end of {}'.format(umi)
        else:
            break
    out = open(js, 'w+')
    out.write(json.dumps(dict_gp))
    out.close()

def main():
    dict_umi = ReadFastq(sys.argv[1])
    print 'end of creating dict_umi'
    HandleUMI(dict_umi, sys.argv[2])

if __name__ == '__main__':
    main()

