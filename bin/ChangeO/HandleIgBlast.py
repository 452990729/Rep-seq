#!/usr/bin/env python


import os
import re
import argparse
import subprocess
from Bio import SeqIO

'''
globle path
'''
IgBlast_path = '/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/igblast'
Ref_path = '/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/RefData'


def RunIgBlast(file_in, specie, typ):
    '''
    run igblastn on the data *.fastq
    '''
    out_name = re.split('\.', os.path.basename(file_in))[0]+'.fasta'
    out = open(out_name, 'w')
    for record in SeqIO.parse(file_in, 'fastq'):
        out.write(">{}\n{}\n".format(record.id,record.seq))
    out.close()
    if typ in ['IGH', 'IGK', 'IGL']:
        ts = 'Ig'
    elif typ in ['TRA', 'TRB']:
        ts = 'TCR'
    db_path = Ref_path+'/'+specie+'/'+typ
    anno_path = Ref_path+'/optional_file'
#    if typ in ['IGH', 'TRB']:
    child1 = subprocess.Popen([os.path.join(IgBlast_path, 'igblastn'),\
                       '-germline_db_V', os.path.join(db_path, 'v.fa'), \
                       '-germline_db_D', os.path.join(db_path, 'd.fa'), \
                       '-germline_db_J', os.path.join(db_path, 'j.fa'), \
                       '-auxiliary_data', os.path.join(anno_path, specie), \
                       '-domain_system', 'imgt', \
                       '-ig_seqtype', ts, '-organism', specie, \
                       '-num_threads', '5', \
                       '-outfmt', '7 std qseq sseq btop', \
                       '-query', out_name, \
                       '-out', re.split('\.', os.path.basename(file_in))[0]+'.fmt7'])
#    elif typ in ['IGK', 'IGL', 'TRA']:
#        child1 = subprocess.Popen([os.path.join(IgBlast_path, 'igblastn'),\
#                       '-germline_db_V', os.path.join(db_path, 'v.fa'), \
#                        '-germline_db_J', os.path.join(db_path, 'j.fa'), \
#                        '-auxiliary_data', os.path.join(anno_path, specie), \
#                        '-domain_system', 'imgt', \
#                        '-ig_seqtype', ts, '-organism', specie, \
#                        '-num_threads', '5', \
#                        '-outfmt', '7 std qseq sseq btop', \
#                        '-query', out_name, \
#                        '-out', re.split('\.', file_in)[0]+'.fmt7'])
    child1.wait()

def main():
    parser = argparse.ArgumentParser(description="the igblast process")
    parser.add_argument('--fq',help="the fastq file", required=True)
    parser.add_argument('--specie',help="the specie", required=True)
    parser.add_argument('--type',help="the type of the analysis",\
                        choices=['IGH', 'IGK', 'IGL', 'TRA', 'TRB'], required=True)
    argv=vars(parser.parse_args())
    RunIgBlast(argv['fq'], argv['specie'], argv['type'])


if __name__ == '__main__':
    main()
