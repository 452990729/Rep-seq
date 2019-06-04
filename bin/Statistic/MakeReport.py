#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from copy import deepcopy
from glob import glob
import xlrd
from jinja2 import Environment, PackageLoader
reload(sys)
sys.setdefaultencoding( "utf-8" )

def PrepareFile(path_in, path_out):
    path_base = glob(path_in+'/*/*/out')
    path_stat = glob(path_in+'/*/*/out/stats')
    name = 'VS'.join([re.split('/', i)[-2] for i in path_base])
    os.system('cp -rf \
              /huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/report/RepReport\
               {}'.format(os.path.join(path_out, name)))
    base_pic = path_out+'/'+name+'/src/pictures'
    base_file = path_out+'/'+name+'/result'
    summary = open(os.path.join(base_file, 'Summary.txt'), 'w+')
    i = 0
    summary.write('\t'.join(['ID', 'Sample', 'ReadPair', 'FilteredReads',\
                             'Clone', 'ClonePercent(%)', 'UniqueV', 'UniqueJ',\
                             'UniqueVDJ', 'UniqueCDR3aa', 'UniqueCDR3nt'])+'\n')
    for sp in path_base:
        i += 1
        sb = re.split('/', sp)[-2]
        sp_stat_path = sp+'/stats'
        os.system('cp {} {}'.format(os.path.join(sp,\
                                                 sb+'.CloneFilter.txt'),\
                                   base_file))
        for png in glob(sp_stat_path+'/*.png'):
            os.system('cp {} {}'.format(png, base_pic))
        for xls in glob(sp_stat_path+'/*.xls'):
            os.system('cp {} {}'.format(xls, base_file))
        with open(os.path.join(sp_stat_path, sb+'.sumary'), 'r') as in1:
            summary.write(str(i)+'\t'+in1.read().strip()+'\n')
    summary.close()
    for png in glob(path_in+'/../Compare/*.png'):
        os.system('cp {} {}'.format(png, base_pic))
    for txt in glob(path_in+'/../Compare/*.txt'):
        os.system('cp {} {}'.format(txt, base_file))
    for xls in glob(path_in+'/../Compare/*.xls'):
        os.system('cp {} {}'.format(xls, base_file))
    return path_out+'/'+name

def HandlePicPath(list_pic, lib_path):
    list_pic_sorted = sorted(list_pic)
    Base = list_pic_sorted[0]
    BasePath = lib_path+'/'+Base
    dict_tmp = {}
    list_tmp = []
    for sp in list_pic_sorted:
        dict_tmp['base'] = sp
        dict_tmp['path'] = lib_path+'/'+sp
        dict_cp = deepcopy(dict_tmp)
        list_tmp.append(dict_cp)
        dict_tmp = {}
    return Base, BasePath, list_tmp


def MakeReport(path_in, tp):
    base_pic = path_in+'/src/pictures'
    base_file = path_in+'/result'
    env = Environment(loader=PackageLoader('jinjatmp', 'templates'))
    template = env.get_template('report.html')
    ScriptPath = os.path.split(os.path.realpath(__file__))[0]
    QCItems = []
    dict_qc = {}
    with open(os.path.join(base_file, 'Summary.txt'), 'r') as in1:
        for line in in1:
            list_split = re.split('\t', line.strip())
            dict_qc['ID'] = list_split[0]
            dict_qc['Sample'] = list_split[1]
            dict_qc['ReadsPair'] = list_split[2]
            dict_qc['FilterReads'] = list_split[3]
            dict_qc['Clone'] = list_split[4]
            dict_qc['ClonePercent'] = list_split[5]
            dict_qc['UniqueV'] = list_split[6]
            dict_qc['UniqueJ'] = list_split[7]
            dict_qc['UniqueVDJ'] = list_split[8]
            dict_qc['UniqueCDR3aa'] = list_split[9]
            dict_qc['UniqueCDR3nt'] = list_split[10]
            dict_cp = deepcopy(dict_qc)
            QCItems.append(dict_cp)
            dict_qc = {}
    clone_file = glob(base_file+'/*.CloneFilter.txt')
    CloneItems = []
    dict_clone = {}
    cl = 0
    with open(clone_file[0], 'r') as in1:
        for line in in1:
            cl += 1
            if cl <= 15:
                list_split = re.split('\t', line.strip())
                dict_clone['cloneid'] = list_split[0]
                dict_clone['cloneCourt'] = list_split[1]
                dict_clone['cloneFrac'] = list_split[2]
                dict_clone['bestV'] = list_split[3]
                dict_clone['bestD'] = list_split[4]
                dict_clone['bestJ'] = list_split[5]
                dict_clone['bestVHitS'] = list_split[6]
                dict_clone['bestDHitS'] = list_split[7]
                dict_clone['bestJhitS'] = list_split[8]
                dict_clone['bestVFamily'] = list_split[9]
                dict_clone['bestDFamily'] = list_split[10]
                dict_clone['bestJFamily'] = list_split[11]
                dict_clone['nSeqCDR3'] = list_split[12]
                dict_clone['aaSeqCDR3'] = list_split[13]
                dict_cp = deepcopy(dict_clone)
                CloneItems.append(dict_cp)
                dict_clone = {}
    def HandelFraction(file_in):
        list_tmp = []
        m = 0
        try:
            with open(file_in, 'r') as f:
                for line in f:
                    m += 1
                    if m <= 15:
                        list_split = re.split('\t', line.strip())
                        list_tmp.append(list_split)
        except IOError:
            pass
        return list_tmp
    CDR3Diff = HandelFraction(os.path.join(base_file, 'ClonetypeFraction.txt'))
    VGeneDiff = HandelFraction(os.path.join(base_file, 'VFraction.txt'))
    VJDiff = HandelFraction(os.path.join(base_file, 'VJFraction.txt'))
    VDJDiff = HandelFraction(os.path.join(base_file, 'VDJFraction.txt'))
    TestDiff = []
    try:
        data = xlrd.open_workbook(os.path.join(base_file, 'MixDiffAnalysis.xls'))
        table = data.sheet_by_name(u'ClonetypeFraction')
        for i in range(table.nrows):
            if i <15:
                TestDiff.append([str(i) for i in table.row_values(i)])
    except IOError:
        pass
    root, dirs, files = next(os.walk(base_pic))
    list_QCPic = []
    list_VDJUsagePic = []
    list_VJCombinationPic = []
    list_mutation = []
    list_ComparisonOfVGene = []
    list_ComparisonOfVJ = []
    list_ComparisonOfVDJ = []
    list_ComparisonOfVFamily = []
    MutationFrequencyPath = 'test'
    PCAPath = 'test'
    for fl in files:
        if fl.startswith('ReadsQuality'):
            list_QCPic.append(fl)
        elif fl.startswith('FractionOfV'):
            list_VDJUsagePic.append(fl)
        elif fl.startswith('DistributionOfVJCombination'):
            list_VJCombinationPic.append(fl)
        elif fl.startswith('CDR3LengthOfAmino'):
            AACDR3LengthPath = 'src/pictures/'+fl
        elif fl.startswith('CDR3LengthOfNucleotide'):
            nCDR3LengthPath = 'src/pictures/'+fl
        elif fl.startswith('Abundance'):
            AbundancePath = 'src/pictures/'+fl
        elif fl.startswith('Diversity'):
            DiversityPath = 'src/pictures/'+fl
        elif fl.startswith('n2venn'):
            nVennPath = 'src/pictures/'+fl
        elif fl.startswith('a2venn'):
            aaVennPath = 'src/pictures/'+fl
        elif fl.startswith('ComparisonOfVGene'):
            list_ComparisonOfVGene.append(fl)
        elif fl.startswith('ComparisonOfVJ'):
            list_ComparisonOfVJ.append(fl)
        elif fl.startswith('ComparisonOfVDJ'):
            list_ComparisonOfVDJ.append(fl)
        elif fl.startswith('ComparisonOfVFamily'):
            list_ComparisonOfVFamily.append(fl)
        elif fl.startswith('MutationFrequencyDistribution'):
            MutationFrequencyPath = 'src/pictures/'+fl
        elif fl.endswith('MutationFrequencyDistribution.png'):
            list_mutation.append(fl)
        elif fl.startswith('PCA'):
            PCAPath = 'src/pictures/'+fl
    QCBase, QCBasePath, QCPic = HandlePicPath(list_QCPic, 'src/pictures')
    VDJUsageBase, VDJUsagePath, VDJUsagePic = HandlePicPath(list_VDJUsagePic,\
                                                           'src/pictures')
    if tp == 2:
        MutationBase, MutationPath, MutationPic = HandlePicPath(list_mutation,\
                                                            'src/pictures')
    else:
        MutationBase, MutationPath, MutationPic = 0, 0, 0
    VJCombinationBase, VJCombinationPath, VJCombinationPic = \
            HandlePicPath(list_VJCombinationPic, 'src/pictures')
    if tp == 0:
        nVennPath,aaVennPath,= 0,0
    ComparisonOfVGeneBase, ComparisonOfVGenePath, ComparisonOfVGenePic = \
            HandlePicPath(list_ComparisonOfVGene, 'src/pictures')
    ComparisonOfVJBase, ComparisonOfVJPath, ComparisonOfVJPic = \
            HandlePicPath(list_ComparisonOfVJ, 'src/pictures')
    ComparisonOfVDJBase, ComparisonOfVDJPath, ComparisonOfVDJPic = \
            HandlePicPath(list_ComparisonOfVDJ, 'src/pictures')
    ComparisonOfVFamilyBase, ComparisonOfVFamilyPath, ComparisonOfVFamilyPic =\
            HandlePicPath(list_ComparisonOfVFamily, 'src/pictures')
    out_html = open(path_in+'/report.html', 'w+')
    html = template.render(tp=tp, QCItems=QCItems, QCBasePath=QCBasePath,\
                           QCBase=QCBase, QCPic=QCPic, CloneItems=CloneItems,\
                          VDJUsagePath=VDJUsagePath,\
                           VDJUsageBase=VDJUsageBase, VDJUsagePic=VDJUsagePic,\
                          VJCombinationPath=VJCombinationPath,\
                          VJCombinationBase=VJCombinationBase,\
                          VJCombinationPic=VJCombinationPic,\
                          AACDR3LengthPath=AACDR3LengthPath,\
                          nCDR3LengthPath=nCDR3LengthPath,\
                          AbundancePath=AbundancePath,\
                          DiversityPath=DiversityPath,\
                          nVennPath=nVennPath, aaVennPath=aaVennPath,\
                           ComparisonOfVGeneBase=ComparisonOfVGeneBase,\
                           ComparisonOfVGenePath=ComparisonOfVGenePath,\
                           ComparisonOfVGenePic=ComparisonOfVGenePic,\
                           ComparisonOfVJBase=ComparisonOfVJBase,\
                           ComparisonOfVJPath=ComparisonOfVJPath,\
                           ComparisonOfVJPic=ComparisonOfVJPic,\
                           ComparisonOfVDJBase=ComparisonOfVDJBase,\
                           ComparisonOfVDJPath=ComparisonOfVDJPath,\
                           ComparisonOfVDJPic=ComparisonOfVDJPic,\
                           ComparisonOfVFamilyBase=ComparisonOfVFamilyBase,\
                           ComparisonOfVFamilyPath=ComparisonOfVFamilyPath,\
                           ComparisonOfVFamilyPic=ComparisonOfVFamilyPic,\
                           CDR3Diff=CDR3Diff, VGeneDiff=VGeneDiff,\
                           VJDiff=VJDiff, VDJDiff=VDJDiff, TestDiff=TestDiff,\
                           PCAPath=PCAPath,\
                           MutationFrequencyPath=MutationFrequencyPath,\
                           MutationBase=MutationBase,\
                           MutationPath=MutationPath,\
                           MutationPic=MutationPic,\
                          )
    out_html.write(html)
    out_html.close()
#    os.system(ScriptPath+'/html2pdf/RemoveMenuBar.py '+path_in+\
#              '/report.html '+path_in+'/report_r.html')
    os.system(ScriptPath+'/html2pdf/html2pdf.sh '+ScriptPath+\
             '/html2pdf/cover_chs.html '+path_in+\
             '/report.html '+path_in+'/report.pdf')
#    os.system('rm '+path_in+'/report_r.html')


def main():
    path_report = PrepareFile(sys.argv[1], sys.argv[2])
    MakeReport(path_report, int(sys.argv[3]))

if __name__ == '__main__':
    main()



