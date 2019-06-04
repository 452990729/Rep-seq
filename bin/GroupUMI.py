#!/usr/bin/env python

import sys
import json
import collections
import argparse
import pp
from config import ReadSam
import workflow

class UMI(object):
    '''
    the UMI data format
    '''
    def __init__(self, id_in, dict_umi):
        self.id = id_in
        self.umi = dict_umi[id_in]


def GenerateUMITable(file_in):
    '''
    read UMI fastq file -> dict[id] = barcode
    '''
    i = 0
    list_tmp = []
    dict_re = {}
    with open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            i += 1
            if i < 4:
                list_tmp.append(line)
            elif i == 4:
                list_tmp.append(line)
                ob = workflow.Fastq(list_tmp)
                dict_re[ob.id] = ob.barcode
                i = 0
                list_tmp = []
    return dict_re

def GenerateIDGroup(file_in, type_receptor):
    '''
    read sam file -> dict[annotation] = [id1,id2,]
    '''
    list_sam = ReadSam(file_in, type_receptor)
    dict_re = {}
    for ob in list_sam:
        if ob.ref not in dict_re:
            dict_re[ob.ref] = [ob.query]
        else:
            dict_re[ob.ref] += [ob.query]
    return [tuple(i) for i in dict_re.values()]

def SplitData(list_in, dict_in):
    '''
    split the data by medean value
    '''
    list_ob_umi = [UMI(i, dict_in) for i in list_in]
    dict_value = dict(collections.Counter([m.umi for m in list_ob_umi]))
    list_up = []
    list_dw = []
    for ob in list_ob_umi:
        if dict_value[ob.umi] >= 3:
            list_up.append(ob.id)
        else:
            list_dw.append(ob.id)
    return list_up, list_dw

def Cose(list_in, dict_in):
    list_up, list_dw = SplitData(list_in, dict_in)
    dict_tmp = {}
    list_tmp = []
    list_out = []
    list_lv = []
    len_ref = len(list_up)
    for ref in list_up:
        dict_tmp[ref] = [ref]
    for query in list_dw:
        i = 0
        for ref in list_up:
            i += 1
            if workflow.Dist(dict_in[query], dict_in[ref], 2):
                dict_tmp[ref] += [query]
                break
        if i == len_ref:
            list_lv.append(query)
    list_out += dict_tmp.values()
    list_out += GenerateUMIGroup(dict_in,list_lv)
    return list_out

def GenerateUMIGroup(dict_in, tuple_in, mismatch=2):
    '''
    group the id by umi similarity -> dict
    '''
    list_re = []
    list_tmp = []
    for i in range(len(tuple_in)):
        if tuple_in[i] not in list_tmp:
            list_group = []
            for query in tuple_in[i:]:
                if  query not in list_tmp and \
                    workflow.Dist(dict_in[tuple_in[i]], dict_in[query], mismatch):
                    list_group.append(query)
                    list_tmp.append(query)
            list_re.append(list_group)
    return list_re

def MultiCompare(dict_in, list_in, num_core, outfile):
    '''
    use pp to run multi core process on UMI grouping
    '''
    ppservers = ()
    list_tmp = []
    list_dt = []
    list_ut = []
    dict_tmp = {}
    for record in list_in:
        if len(record) == 1:
            list_tmp.append(record)
        elif len(record) >= 10000:
            list_ut.append(record)
        else:
            list_dt.append(record)
    out = open(outfile, 'w+')
    job_server = pp.Server(num_core, ppservers=ppservers)
    jobs = [(job_server.submit(GenerateUMIGroup, (dict_in, tuple_in), (),\
                               ("workflow",))) for tuple_in in list_dt]
    for job in jobs:
        list_tmp += job()
    jobs2 = [(job_server.submit(Cose, (list_in, dict_in), (SplitData, UMI, GenerateUMIGroup),\
                               ("workflow", "collections"))) for list_in in list_ut]
    for job in jobs2:
        list_tmp += job()
    for s in list_tmp:
        for m in s:
            dict_tmp[m] = dict_in[s[0]]
    out.write(json.dumps(dict_tmp))

def main():
    parser = argparse.ArgumentParser(description="group the similar UMIs")
    parser.add_argument('--umi',help="the umi fastq", required=True)
    parser.add_argument('--sam',help="the bowtie output sam", required=True)
    parser.add_argument('--type',help="the type of the analysis",\
                        choices=['IG', 'TR'], required=True)
    parser.add_argument('--core',help="the output file", default=20)
    parser.add_argument('--out',help="the output file", required=True)
    argv=vars(parser.parse_args())
    dict_umi = GenerateUMITable(argv['umi'])
    list_umi = GenerateIDGroup(argv['sam'], argv['type'])
    MultiCompare(dict_umi, list_umi, int(argv['core']), argv['out'])


if __name__ == '__main__':
    main()
