#!/ifs/TJPROJ3/DENOVO/lixuefei/soft/anaconda2/bin/python2

import re
import argparse
import json
from workflow import Fastq, Json2Str

def ReadFastq(file_in):
    '''
    read the fastq data -> dict[fastq.id]=Fastq(object)
    '''
    i = 0
    list_tmp = []
    dict_tmp = {}
    with open(file_in, 'r') as in1:
        for line in in1:
            line = line.strip()
            i += 1
            if i < 4:
                list_tmp.append(line)
            elif i == 4:
                list_tmp.append(line)
                ob = Fastq(list_tmp)
                dict_tmp[ob.id] = ob
                i = 0
                list_tmp = []
    return dict_tmp

def ReadUMI(file_in):
    '''
    read the group UMI.json
    return dict
    '''
    dict_tmp = {}
    with open(file_in, 'r') as in1:
        dict_tmp = Json2Str(json.load(in1))
    return dict_tmp

def Paired(dict_s1, dict_s2, dict_UMI, file_out1, file_out2):
    '''
    paired the seq
    write out the format fastq data
    '''
    set_ds = set(dict_s1.keys())&set(dict_s2.keys())&set(dict_UMI.keys())
    out1 = open(file_out1, 'w+')
    out2 = open(file_out2, 'w+')
    i = 0
    for key in set_ds:
        umi = dict_UMI[key]
        out1.write(dict_s1[key].MakeFs(umi)+'\n')
        out2.write(dict_s2[key].MakeFs(umi)+'\n')
    out1.close()
    out2.close()

def ChangeName(string_in):
    '''
    change the output name
    return string
    '''
    list_tmp = re.split('\.', string_in)
    return '.'.join(list_tmp[:-1])+'_paired-pass'+'.'+list_tmp[-1]

def main():
    parser = argparse.ArgumentParser(description="instead the PairSeq.py of\
                                     pRESTO pipeline")
    parser.add_argument('--f1',help="the fastq1", required=True)
    parser.add_argument('--f2',help="the fastq2", required=True)
    parser.add_argument('--umi',help="the uniq umi", required=True)
    argv=vars(parser.parse_args())
    dict1 = ReadFastq(argv['f1'])
    dict2 = ReadFastq(argv['f2'])
    dict_UMI = ReadUMI(argv['umi'])
    Paired(dict1, dict2, dict_UMI, ChangeName(argv['f1']), ChangeName(argv['f2']))


if __name__ == '__main__':
    main()
