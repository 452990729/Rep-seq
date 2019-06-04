#!/usr/bin/env python


import sys
import os
import re
import gzip
from glob import glob
import xlwt

def GetTheLengthOfFile(file_in):
    count = 0
    if file_in.endswith('.gz'):
        f1 = gzip.open(file_in, 'rb')
    else:
        f1 = open(file_in, 'rb')
    while True:
        buffers = f1.read(1024 * 8192)
        if not buffers:
            break
        count += buffers.count('\n')
    f1.close()
    return count

def GetSummary(path_in, list_in, Sample):
    ReadPair = GetTheLengthOfFile(list_in[0])/4
    pass_pair = glob(path_in+'/3.GetSeq/*_quality-pass_pair-pass.fastq')[0]
    FilteredReads = GetTheLengthOfFile(pass_pair)/4
    list_uniqueCDR3aa = []
    list_uniqueCDR3nt = []
    Clones = 0
    Clonetypes = 0
    with open(os.path.join(path_in, '5.stats/'+Sample+'.clonetype.filter.txt'), 'r') as cl:
        for line in cl.readlines()[1:]:
            list_split = re.split('\t', line.strip())
            Clones += int(list_split[1])
            if list_split[-2] not in list_uniqueCDR3nt:
                list_uniqueCDR3nt.append(list_split[-2])
            if list_split[-1] not in list_uniqueCDR3aa:
                list_uniqueCDR3aa.append(list_split[-1])
            Clonetypes += 1
    UniqueCDR3aa = len(list_uniqueCDR3aa)
    UniqueCDR3nt = len(list_uniqueCDR3nt)
#    ClonePercent = round(float(Clone)*100/ReadPair, 2)
    UniqueV = GetTheLengthOfFile(path_in+'/5.stats/'+Sample+'.V.stat')
    UniqueJ = GetTheLengthOfFile(path_in+'/5.stats/'+Sample+'.J.stat')
    UniqueVDJ = GetTheLengthOfFile(path_in+'/5.stats/'+Sample+'.VDJCom.stat')
    ReadUtilization = round(float(FilteredReads)*100/ReadPair, 2)
    out = open(path_in+'/5.stats/'+Sample+'.sumary', 'w')
    out.write('\t'.join([str(i) for i in [Sample, ReadPair, FilteredReads,\
                                          ReadUtilization, Clones, Clonetypes,\
                        UniqueV, UniqueJ, UniqueVDJ, UniqueCDR3aa,\
                                          UniqueCDR3nt]]))
    out.close()

def ExcelStyle(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def WriteExcelSheet(sheet, file_in):
    m = 0
    default = ExcelStyle('Times New Roman',220,True)
    with open(file_in, 'r') as in1:
        for line in in1:
            m += 1
            list_split = re.split('\t', line.strip())
            for i in range(0, len(list_split)):
                sheet.write(m, i, list_split[i], default)

def GetUsage(path_in, Sample):
    V = path_in+'/5.stats/'+Sample+'.V.stat'
    D = path_in+'/5.stats/'+Sample+'.D.stat'
    J = path_in+'/5.stats/'+Sample+'.J.stat'
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'V',cell_overwrite_ok=True)
    row0 = ['Gene', 'Count', 'Frequency']
    for i in range(0,len(row0)):
        sheet1.write(0, i, row0[i], ExcelStyle('Times New Roman',220,True))
    WriteExcelSheet(sheet1, V)
    sheet2 = f.add_sheet(u'D',cell_overwrite_ok=True)
    for i in range(0,len(row0)):
        sheet2.write(0, i, row0[i], ExcelStyle('Times New Roman',220,True))
    WriteExcelSheet(sheet2, D)
    sheet3 = f.add_sheet(u'J',cell_overwrite_ok=True)
    for i in range(0,len(row0)):
        sheet3.write(0, i, row0[i], ExcelStyle('Times New Roman',220,True))
    WriteExcelSheet(sheet3, J)
    f.save(path_in+'/5.stats/'+Sample+'_VDJUsage.xls')

def GetCombination(path_in, Sample):
    VJ = path_in+'/5.stats/'+Sample+'.VJCom.stat'
    VDJ = path_in+'/5.stats/'+Sample+'.VDJCom.stat'
    f = xlwt.Workbook()
    default = ExcelStyle('Times New Roman',220,True)
    sheet1 = f.add_sheet(u'VJ',cell_overwrite_ok=True)
    row0 = ['V gene', 'J gene', 'Count', 'Frequency']
    for i in range(0,len(row0)):
        sheet1.write(0, i, row0[i], default)
    WriteExcelSheet(sheet1, VJ)
    sheet2 = f.add_sheet(u'VDJ',cell_overwrite_ok=True)
    row0 = ['V gene', 'D gene', 'J gene', 'Count', 'Frequency']
    for i in range(0,len(row0)):
        sheet2.write(0, i, row0[i], default)
    WriteExcelSheet(sheet2, VDJ)
    f.save(path_in+'/5.stats/'+Sample+'_VDJCombination.xls')

def main():
    raw_list = re.split(',', sys.argv[3])
    name = sys.argv[2]
    GetSummary(sys.argv[1], raw_list, name)
    GetUsage(sys.argv[1], name)
    GetCombination(sys.argv[1], name)


if __name__ == '__main__':
    main()




