#!/usr/bin/env python


import sys
import argparse
from align import Bowtie2Reference

def Process(path1, path2, path3, path4):
    '''
    path1 -> reference seq
    path2 -> read1
    path3 -> read2
    path4 -> output path
    '''
    BW = Bowtie2Reference()
    BW = BW.load_from_fasta(path1)
    BW.align_reads_paired(path2, path3, path4, write_sam=True, p=10)

def main():
    parser = argparse.ArgumentParser(description="ailgn seq use bowtie")
    parser.add_argument('--ref',help="the reference fasta", required=True)
    parser.add_argument('--f1',help="the input fastq1", required=True)
    parser.add_argument('--f2',help="the input fastq2", required=True)
    parser.add_argument('--out',help="the output file", required=True)
    argv=vars(parser.parse_args())
    Process(argv['ref'], argv['f1'], argv['f2'], argv['out'])


if __name__ == '__main__':
    main()

