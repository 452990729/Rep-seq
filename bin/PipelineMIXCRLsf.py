#!/usr/bin/env python2

import re
import sys
import os
import time
from glob import glob
import argparse

class FastqList(object):
    def __init__(self, line_in):
        list_tmp = re.split('\s+', line_in)
        self.name = list_tmp[0]
        self.group = list_tmp[1]
        self.fastq = list_tmp[2]

def QC(BinPath, FastqPath, ShellPath, OutPath):
    list_fastq = re.split(',', FastqPath)
    out = open(os.path.join(ShellPath, 'QC.sh'), 'w+')
    list_base = []
    i = 0
    for fastq in list_fastq:
        i += 1
        out.write('{} quality -s {} -q 20 --outname {} --log {}\
                  --nproc 5 --outdir {}'.format(os.path.join(BinPath, 'FilterSeq.py'),\
                  fastq, re.split('\.',os.path.basename(fastq))[0],\
                  'QC'+str(i)+'.log', OutPath)+'\n')
        list_base.append(re.split('\.', os.path.basename(fastq))[0])
    out.close()
    return list_base

def PairSeq(BinPath, list_base, ShellPath, tp, OutPath):
    assert len(list_base) == 2
    out = open(os.path.join(ShellPath, 'PairSeq.sh'), 'w+')
    out.write('{} -l {} {} -f ID QUALITY --outdir {}'\
             .format(os.path.join(BinPath, 'ParseLog.py'),\
                     OutPath+'/../bsub.QC/QC1.log', \
                     OutPath+'/../bsub.QC/QC2.log', OutPath)+'\n')
    out.write('{} -1 {} -2 {} --coord {} --outdir {}'.format(os.path.join(BinPath,\
            'PairSeq.py'), OutPath+'/'+list_base[0]+'_quality-pass.fastq', \
            OutPath+'/'+list_base[1]+'_quality-pass.fastq', tp, OutPath))
    out.close()

def Mixcr(BinPath, list_base, ShellPath, tp, speice, OutPath):
    assert len(list_base) == 2
    out = open(os.path.join(ShellPath, 'Mixcr.sh'), 'w+')
    out.write('{} align -r align.txt -c {} -s {} -t 5 --library imgt \
        {} {} {}'.format(BinPath+'/Mixcr/mixcr-2.1.5/mixcr',\
        tp, speice, OutPath+'/'+list_base[0]+'_quality-pass_pair-pass.fastq', \
        OutPath+'/'+list_base[1]+'_quality-pass_pair-pass.fastq', \
        os.path.join(OutPath, 'alignments.vdjca'))+'\n')
    out.write('{} assemble -r assemble.txt -t 4 {} {}'\
             .format(BinPath+'/Mixcr/mixcr-2.1.5/mixcr', \
                    os.path.join(OutPath, 'alignments.vdjca'),\
                    os.path.join(OutPath, 'clones.clns'))+'\n')
    out.write('{} exportClones -cloneId -count -fraction -vGene -dGene \
              -jGene -vHitScore -dHitScore -jHitScore -vFamily -dFamily \
              -jFamily -nFeature CDR3 -aaFeature CDR3 {} \
              {}'.format(BinPath+'/Mixcr/mixcr-2.1.5/mixcr', \
              OutPath+'/clones.clns', \
              OutPath+'/'+re.split('_', list_base[0])[0]+'.clones.txt'))
    out.close()

def FilterAndStat(BinPath, base, ShellPath, OutPath):
    out = open(os.path.join(ShellPath, 'FilterAndStat.sh'), 'w+')
    out.write(BinPath+'/Mixcr/MixcrFliter.py '+\
              os.path.join(OutPath, base+'.clones.txt')+' '+OutPath+'\n')
    out.write(BinPath+'/Statistic/MakeStatMixcr.py '+\
             os.path.join(OutPath, base+'.CloneFilter.txt')+' '+base+' '+\
             OutPath+'/stats'+'\n')
    out.write(BinPath+'/Mixcr/Mixcr2Alakazam.py '+\
             os.path.join(OutPath, base+'.CloneFilter.txt')+' '+OutPath)
    out.close()

def MakeSingle(BinPath, base, ShellPath, OutPath, FastqPath):
    pic_path = OutPath+'/stats'
    out = open(os.path.join(ShellPath, 'PlotSingle.sh'), 'w+')
    out.write(BinPath+'/Statistic/QcPlot.py '+OutPath+' '+base+\
              ' '+pic_path+'\n')
    out.write(BinPath+'/Statistic/StatPlotMixcr.py PlotVDJ '+pic_path+\
              ' '+base+'\n')
    out.write(BinPath+'/Statistic/StatPlotMixcr.py PlotVJComb '+pic_path+\
              ' '+base+'\n')
    out.write(BinPath+'/Statistic/MakeFinal.py '+OutPath+' '+FastqPath)
    out.close()

def PlotMulti(BinPath, InPath, OutPath):
    path_stat = glob(InPath+'/analysis/*/*/out/stats')
    path_clone = glob(InPath+'/analysis/*/*/out/*.CloneFilter.txt')
    out = open(os.path.join(InPath, 'Multi.sh'), 'w+')
    out.write(BinPath+'/Statistic/StatPlotMixcr.py PlotCDR3Bar '+\
              ','.join(path_stat)+' a '+OutPath+'\n')
    out.write(BinPath+'/Statistic/StatPlotMixcr.py PlotCDR3Bar '+\
              ','.join(path_stat)+' n '+OutPath+'\n')
    out.write(BinPath+'/individualization/VennPlotMixcr.py n '+\
              ' '.join(path_clone)+' '+OutPath+'\n')
    out.write(BinPath+'/individualization/VennPlotMixcr.py a '+\
              ' '.join(path_clone)+' '+OutPath+'\n')
    out.close()

def PlotCorr(BinPath, gp1, gp2, InPath, OutPath):
    gp1_path = '/'.join([InPath, 'analysis', gp1, 'out'])
    gp2_path = '/'.join([InPath, 'analysis', gp2, 'out'])
    gn1 = re.split('/', gp1)[-1]
    gn2 = re.split('/', gp2)[-1]
    out = open(os.path.join(InPath, 'Corr.sh'), 'a+')
    out.write(BinPath+'/individualization/CompareVMixcr.py VGene '+\
             gp1_path+'/stats/'+gn1+'.V.stat '+\
             gp2_path+'/stats/'+gn2+'.V.stat '+OutPath+'\n')
    out.write(BinPath+'/individualization/CompareVMixcr.py VJ '+\
              gp1_path+'/stats/'+gn1+'.VJCom.stat '+\
              gp2_path+'/stats/'+gn2+'.VJCom.stat '+OutPath+'\n')
    out.write(BinPath+'/individualization/CompareVMixcr.py VDJ '+\
              gp1_path+'/stats/'+gn1+'.VDJCom.stat '+\
              gp2_path+'/stats/'+gn2+'.VDJCom.stat '+OutPath+'\n')
    out.write(BinPath+'/individualization/CompareVMixcr.py VFamily '+\
              gp1_path+'/stats/'+gn1+'.VFamily.stat '+\
              gp2_path+'/stats/'+gn2+'.VFamily.stat '+OutPath+'\n')
    out.close()

def DivAndAbun(BinPath, InPath, OutPath):
    out = open(os.path.join(InPath, 'DivAndAbun.sh'), 'w+')
    out.write(BinPath+'/Mixcr/CatAlakazam.py '+InPath+' '+OutPath+'\n')
    out.write('Rscript '+BinPath+'/individualization/DivAndAbun.R '+\
            os.path.join(OutPath, 'alakazam.out')+\
            ' '+OutPath+'/Abundance.pdf '+\
             OutPath+'/Diversity.pdf'+'\n')
    out.write(' '.join(['convert', OutPath+'/Abundance.pdf', \
                        OutPath+'/Abundance.png'])+'\n')
    out.write(' '.join(['convert', OutPath+'/Diversity.pdf', \
                        OutPath+'/Diversity.png']))
    out.close()

def GetMutation(BinPath, InPath, OutPath):
    out = open(os.path.join(InPath, 'GetMutation.sh'), 'w+')
    paths = glob(InPath+'/analysis/*/*/out')
    path_vdj = []
    for path in paths:
        label = re.split('/', path)[-2]
        out.write(' '.join([BinPath+'/Mixcr/mixcr-2.1.5/mixcr',\
                'exportAlignments', '-vHit', '-nFeature VDJRegion',\
                '-vAlignment', '-aaFeature FR1', '-aaFeature CDR1',\
                '-aaFeature FR2', '-aaFeature CDR2',\
                '-aaFeature FR3', '-aaFeature CDR3', '-aaFeature FR4',\
                os.path.join(path, 'alignments.vdjca'),\
                os.path.join(path, label+'.VDJRegion.txt')])+'\n')
        path_vdj.append(os.path.join(path, label+'.VDJRegion.txt'))
    out.write(BinPath+'/Mixcr/VhAlignMismatch.py '+' '.join(path_vdj)+\
             ' '+OutPath+'\n')
    path_v = glob(InPath+'/analysis/*/*/out/stats/*.V.stat')
    list_vh = []
    for path in path_v:
        i = 0
        with open(path, 'r') as f:
            for line in f:
                i += 1
                if i <=6:
                    list_vh.append(re.split('\t', line)[0])
    str_vh = ','.join(list(set(list_vh)))
    out.write(BinPath+'/Mixcr/VhMismatchCount.py '+' '.join(path_vdj)+\
             ' '+str_vh+' '+OutPath+'\n')
    out.close()

def MakeReport(BinPath, InPath, tp):
#    gn1 = re.split('/', gp1)[-1]
#    gn2 = re.split('/', gp2)[-1]
    out = open(os.path.join(InPath, 'report.sh'), 'w+')
    outpath = os.path.join(InPath, 'Report')
    out.write(BinPath+'/Statistic/MakeReport.py '+InPath+'/analysis '+outpath+\
              ' '+str(tp))
    out.close()

def ArgparseLine():
    parser = argparse.ArgumentParser(description="ReqSeq pipeline")
    parser.add_argument('--type',help="the type of the analysis",\
                         choices=['IGH', 'TRA', 'TRB', 'TRD', 'IGK', 'IGL'],\
                        required=True)
    parser.add_argument('--specie',help="the specie",\
                        choices=['hsa', 'mmu', 'rat', 'zebrafish']  ,required=True)
    parser.add_argument('--list',help="the input fastq list", required=True)
    parser.add_argument('--outdir',help="the output dir", required=True)
    parser.add_argument('--datatype',\
                        choices=['illumina','solexa','sra','454','presto'],\
                                 help="the fastq type", required=True)
    parser.add_argument('--compare', choices=['0', '1'],\
                        default=0, help="whether compare group", required=True)
    parser.add_argument('--run', choices=['0', '1'],\
                        default=1, help="whether run shell right now", required=True)
    parser.add_argument('--advanced', choices=['0', '1'],\
                        default=0, help="whether do advanced analysis", required=True)
    argv=vars(parser.parse_args())
    return argv



def main():
    argv = ArgparseLine()
    BinPath = '/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin'
    outdir = argv['outdir']
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    AnalysisDir = os.path.join(outdir, 'analysis')
    if not os.path.exists(AnalysisDir):
        os.mkdir(AnalysisDir)
    bsub = '/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/bsub.sh'
    bs = '/huayin/project/HUAYIN/lixuefei/Pipeline/RepSeq/bin/bsub2.sh'
    CompareDir = os.path.join(outdir, 'Compare')
    if not os.path.exists(CompareDir):
        os.mkdir(CompareDir)
    ReportDir = os.path.join(outdir, 'Report')
    if not os.path.exists(ReportDir):
        os.mkdir(ReportDir)
    list_ob = []
    with open(argv['list'], 'r') as f:
        for line in f:
            if not line.startswith('#'):
                list_ob.append(FastqList(line.strip()))
        for ob in list_ob:
            GroupDir = os.path.join(AnalysisDir, ob.group)
            if not os.path.exists(GroupDir):
                os.mkdir(GroupDir)
            SingleDir = os.path.join(GroupDir, ob.name)
            if not os.path.exists(SingleDir):
                os.mkdir(SingleDir)
            ShellDir = os.path.join(SingleDir, 'shell')
            if not os.path.exists(ShellDir):
                os.mkdir(ShellDir)
            OutDir = os.path.join(SingleDir, 'out')
            if not os.path.exists(OutDir):
                os.mkdir(OutDir)
            StatsDir=os.path.join(OutDir, 'stats')
            if not os.path.exists(StatsDir):
                os.mkdir(StatsDir)
            allshell = open(os.path.join(SingleDir, 'all.sh'), 'w+')
            os.chdir(SingleDir)
            allshell.write('echo ========Start QC at : `date`========'+'\n')
            list_base = QC(BinPath, ob.fastq, ShellDir, OutDir)
            allshell.write(' '.join([bsub, os.path.join(ShellDir, 'QC.sh'), \
                                    '5', 'QC'])+'\n')
            allshell.write('echo ========End QC at : `date`========'+'\n'+\
                           'echo ========Start PairSeq at : `date`========'+'\n')
            PairSeq(BinPath, list_base, ShellDir, argv['datatype'], OutDir)
            allshell.write(' '.join([bsub, os.path.join(ShellDir,'PairSeq.sh'),\
                                     '1', 'PairSeq'])+'\n')
            allshell.write('echo ========End PairSeq at : `date`========'+'\n'+\
                          ' echo ========Start Mixcr at : `date`========'+'\n')
            Mixcr(BinPath, list_base, ShellDir, argv['type'], argv['specie'], OutDir)
            allshell.write(' '.join([bs, os.path.join(ShellDir, 'Mixcr.sh'),\
                                    '5', 'Mixcr'])+'\n')
            allshell.write('echo ========End Mixcr at : `date`========'+'\n'+\
                           'echo ========Start FilterAndStat at : `date`========'+'\n')
            FilterAndStat(BinPath, ob.name, ShellDir, OutDir)
            allshell.write(' '.join([bs, os.path.join(ShellDir,\
                                    'FilterAndStat.sh'), '1', 'FilterAndStat'])+'\n')
            allshell.write('echo ========End FilterAndStat at : `date`========'+'\n'+\
                           'echo ========Start MakeSingle at : `date`========'+'\n')
            MakeSingle(BinPath, ob.name, ShellDir, OutDir, ob.fastq)
            allshell.write(' '.join([bs, os.path.join(ShellDir,\
                                    'PlotSingle.sh'), '1', 'PlotSingle'])+'\n')
            allshell.write('echo ========End MakeSingle at :\
                           `date`========'+'\n'+'echo JOBS DONE')
            allshell.close()
            if int(argv['run']):
                os.popen('nohup sh all.sh 1> stdout.log 2>stderr.log&')
    time.sleep(10)
    if int(argv['compare']):
        nohup_path = glob(AnalysisDir+'/*/*/stdout.log')
        def check(fl):
            with open(fl, 'r') as f:
                a = f.readlines()[-1]
                if not a.startswith('JOBS'):
                    time.sleep(180)
                    check(fl)
                else:
                    pass
        for nohup in nohup_path:
            check(nohup)
        root, dirs, files = next(os.walk(AnalysisDir))
        i = 0
        for dir_s in dirs:
            root2, dirs2, files2 = next(os.walk(os.path.join(root, dir_s)))
            for dir_a in dirs2:
                i += 1
                locals()['gp'+str(i)] = dir_s+'/'+dir_a
        os.chdir(outdir)
        CompareShell = open(os.path.join(outdir, 'Compare.sh'), 'w+')
        CompareShell.write('echo ========Start Compare at : `date`========'+'\n')
        for a in range(1, i+1):
            for b in range(a+1, i+1):
                PlotCorr(BinPath, locals()['gp'+str(a)],\
                         locals()['gp'+str(b)], outdir, CompareDir)
        CompareShell.write(' '.join([bs, os.path.join(outdir,\
                                    'Corr.sh'), '1', 'Corr'])+'\n')
        PlotMulti(BinPath, outdir, CompareDir)
        CompareShell.write(' '.join([bs, os.path.join(outdir,\
                                     'Multi.sh'), '1', 'Multi'])+'\n')
        DivAndAbun(BinPath, outdir, CompareDir)
        CompareShell.write(' '.join([bs, os.path.join(outdir,\
                                'DivAndAbun.sh'), '1', 'DivAndAbun'])+'\n')
        if int(argv['advanced']):
            GetMutation(BinPath, outdir, CompareDir)
            CompareShell.write(' '.join([bs, os.path.join(outdir,\
                            'GetMutation.sh'), '1', 'GetMutation'])+'\n')
        CompareShell.write('echo ========End Compare at : `date`========'+'\n')
        CompareShell.close()
        if int(argv['run']):
            os.system('nohup sh Compare.sh&')
    if int(argv['advanced']):
        tp = 2
    elif int(argv['compare']):
        tp = 1
    else:
        tp = 0
    ReportShell = open(os.path.join(outdir, 'Report.sh'), 'w+')
    ReportShell.write('echo ========Start Report at : `date`========'+'\n')
    MakeReport(BinPath, outdir, tp)
    ReportShell.write(' '.join([bs, os.path.join(outdir,\
                        'report.sh'), '1', 'report'])+'\n')
    ReportShell.write('echo ========End Report at : `date`========'+'\n'+\
                          'echo ALL JOBS DONE')
    CompareShell.close()
    if int(argv['run']):
        os.system('nohup sh Reprot.sh&')


if __name__ == '__main__':
    main()

