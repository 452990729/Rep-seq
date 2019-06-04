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

def CutPrimer(BinPath, ob, ShellPath, outpath):
    list_fastq = re.split(',', ob.fastq)
    Forward = BinPath+'/Race/PRIMER/'+'/ForwardPrime.fa'
    Reverse = BinPath+'/Race/PRIMER/'+'/ReversePrimer.fa'
    CUTP = BinPath+'/Race/CutPrime.py'
    OutPath = os.path.join(outpath, '1.CutPrimer')
    if not os.path.exists(OutPath):
        os.mkdir(OutPath)
    cut1_1 = os.path.join(OutPath, ob.name+'_R1_1_CutPrime.fastq')
    cut1_2 = os.path.join(OutPath, ob.name+'_R1_2_CutPrime.fastq')
    cut2_1 = os.path.join(OutPath, ob.name+'_R2_1_CutPrime.fastq')
    cut2_2 = os.path.join(OutPath, ob.name+'_R2_2_CutPrime.fastq')
    cut1 = os.path.join(OutPath, ob.name+'_R1_CutPrime.fastq')
    cut2 = os.path.join(OutPath, ob.name+'_R2_CutPrime.fastq')
    out = open(os.path.join(ShellPath, '1.CutPrimer.sh'), 'w+')
    out.write('cd {}\n'.format(OutPath))
    out.write(' '.join([CUTP, Forward, list_fastq[0], cut1_1])+'\n')
    out.write(' '.join([CUTP, Reverse, list_fastq[0], cut1_2])+'\n')
    out.write(' '.join([CUTP, Forward, list_fastq[1], cut2_1])+'\n')
    out.write(' '.join([CUTP, Reverse, list_fastq[1], cut2_2])+'\n')
    out.write('cat {} {} > {}\n'.format(cut1_1, cut2_1, cut1))
    out.write('cat {} {} > {}\n'.format(cut1_2, cut2_2, cut2))
    out.write(BinPath+'/Race/FilterPrimerAlign.py '+cut1+' '+ob.name+'_R1_CutPrime_FilterPrimer.fastq\n')
    out.write(BinPath+'/Race/FilterPrimerAlign.py '+cut2+' '+ob.name+'_R2_CutPrime_FilterPrimer.fastq\n')
    out.close()

def QC(BinPath, ob, ShellPath, outpath):
    out = open(os.path.join(ShellPath, '2.QC.sh'), 'w+')
    OutPath = os.path.join(outpath, '2.QC')
    fq1 = os.path.join(outpath, '1.CutPrimer/'+ob.name+'_R1_CutPrime_FilterPrimer.fastq')
    fq2 = os.path.join(outpath, '1.CutPrimer/'+ob.name+'_R2_CutPrime_FilterPrimer.fastq')
    if not os.path.exists(OutPath):
        os.mkdir(OutPath)
    out.write('cd {}\n'.format(OutPath))
    out.write('{} quality -s {} -q 20 --outname {} --log {} --nproc 5 --outdir {}\n'\
              .format(BinPath+'/Race/FilterSeq.py', fq1, ob.name+'_R1', 'QC1.log', OutPath))
    out.write('{} quality -s {} -q 20 --outname {} --log {} --nproc 5 --outdir {}\n'\
              .format(BinPath+'/Race/FilterSeq.py', fq2, ob.name+'_R2', 'QC2.log', OutPath))
    out.write('{} -l {} {} -f ID QUALITY --outdir {}'.format(BinPath+'/Race/ParseLog.py',\
                                                            'QC1.log', 'QC2.log', OutPath))
    out.close()

def GetSeq(BinPath, ob, ShellPath, outpath):
    out = open(os.path.join(ShellPath, '3.GetSeq.sh'), 'w+')
    OutPath = os.path.join(outpath, '3.GetSeq')
    if not os.path.exists(OutPath):
        os.mkdir(OutPath)
    out.write('cd {}\n'.format(OutPath))
    out.write(BinPath+'/Race/ExtractUMI.py '+outpath+'/2.QC/'+ob.name+'_R1_quality-pass.fastq\n')
    out.write(BinPath+'/Race/AlignUMI.py '+ob.name+'_R1_quality-pass_UMI.fastq umi.json\n')
    out.write(BinPath+'/Race/CorrectUMI2.py '+outpath+'/2.QC/'+ob.name+'_R1_quality-pass.fastq umi.json\n')
    out.write(BinPath+'/Race/PairSeq.py -1 '+ob.name+'_R1_quality-pass_CorrectUMI.fastq -2 '+\
              outpath+'/2.QC/'+ob.name+'_R2_quality-pass.fastq --outdir '+OutPath+' --1f BARCODE --coord illumina\n')
    out.write(BinPath+'/Race/SelectData.py '+ob.name+'_R1_quality-pass_CorrectUMI_pair-pass.fastq\n')
    out.write(BinPath+'/Race/SelectData.py '+ob.name+'_R2_quality-pass_pair-pass.fastq\n')
    out.write(BinPath+'/Race/AlignSets.py muscle -s '+ob.name+'_R1_quality-pass_CorrectUMI_pair-pass_select.fastq '+\
             '--exec '+BinPath+'/Race/muscle --outname '+ob.name+'_R1 --log AS1.log\n')
    out.write(BinPath+'/Race/AlignSets.py muscle -s '+ob.name+'_R2_quality-pass_pair-pass_select.fastq '+\
              '--exec '+BinPath+'/Race/muscle --outname '+ob.name+'_R2 --log AS2.log\n')
    out.write(BinPath+'/Race/BuildConsensus.py -s '+ob.name+'_R1_align-pass.fastq '+\
              '--bf BARCODE --maxerror 0.1 --maxgap 0.5 --outname '+ob.name+'_R1 --log BC1.log\n')
    out.write(BinPath+'/Race/BuildConsensus.py -s '+ob.name+'_R2_align-pass.fastq '+\
              '--bf BARCODE --maxerror 0.1 --maxgap 0.5 --outname '+ob.name+'_R2 --log BC2.log\n')
    out.write(BinPath+'/Race/PairSeq.py -1 '+ob.name+'_R1_consensus-pass.fastq -2 '+\
              ob.name+'_R2_consensus-pass.fastq --coord presto\n')
    out.write(BinPath+'/Race/AssemblePairs.py join -1 '+ob.name+'_R1_consensus-pass_pair-pass.fastq -2 '+\
              ob.name+'_R2_consensus-pass_pair-pass.fastq --coord presto --rc tail --1f CONSCOUNT '+\
              '--2f CONSCOUNT --outname '+ob.name+'_R12 --log AP.log --outdir ./\n')
    out.write(BinPath+'/Race/ParseHeaders.py collapse -s '+ob.name+'_R12_assemble-pass.fastq -f CONSCOUNT --act min\n')
    out.write(BinPath+'/Race/CorrectConscount.py '+ob.name+'_R1_quality-pass_CorrectUMI_pair-pass_select.json '+\
              ob.name+'_R2_quality-pass_pair-pass_select.json '+ob.name+'_R12_assemble-pass_reheader.fastq '+\
              ob.name+'_R12_assemble-pass_reheader_correct.fastq\n')
    out.write(BinPath+'/Race/CollapseSeq.py -s '+ob.name+'_R12_assemble-pass_reheader_correct.fastq --inner '+\
              '--cf CONSCOUNT --act sum --outname '+ob.name+'_R12 -n 20\n')
    out.write(BinPath+'/Race/SplitSeq.py group -s '+ob.name+'_R12_collapse-unique.fastq -f CONSCOUNT --num 2 '+\
              '--outname '+ob.name+'_R12\n')
    out.write(BinPath+'/Race/ParseHeaders.py table -s '+ob.name+'_R12_atleast-2.fastq -f ID CONSCOUNT DUPCOUNT\n')
    out.close()

def Annotation(BinPath, ob, tp, spe, ShellPath, outpath):
    out = open(os.path.join(ShellPath, '4.Annotation.sh'), 'w+')
    OutPath = os.path.join(outpath, '4.Annotation')
    if not os.path.exists(OutPath):
        os.mkdir(OutPath)
    out.write('cd {}\n'.format(OutPath))
    out.write(BinPath+'/ChangeO/HandleIgBlast.py --fq '+outpath+'/3.GetSeq/'+ob.name+'_R12_atleast-2.fastq '+\
             '--specie '+spe+' --type '+tp+'\n')
    out.write(BinPath+'/ChangeO/MakeDb.py igblast -i '+ob.name+'_R12_atleast-2.fmt7 -r '+\
              BinPath+'/../RefData/'+spe+'/'+tp+' -s '+ob.name+'_R12_atleast-2.fasta --regions --scores --cdr3\n')
    out.write(BinPath+'/ChangeO/ParseDb.py split -d '+ob.name+'_R12_atleast-2_db-pass.tab -f FUNCTIONAL\n')
    if tp in ['IGH', 'IGK', 'IGL']:
        out.write(BinPath+'/ChangeO/DefineClones.py bygroup -d '+ob.name+'_R12_atleast-2_db-pass_FUNCTIONAL-T.tab '+\
                  '--act set --model ham --sym min --norm len --dist 0.16\n')
    elif tp in ['TRA', 'TRB']:
        out.write(BinPath+'/ChangeO/HandleTCR.py --in '+ob.name+'_R12_atleast-2_db-pass_FUNCTIONAL-T.tab\n')
    out.close()

def MakeSingle(BinPath, ob, ShellPath, outpath):
    out = open(os.path.join(ShellPath, '5.Single.sh'), 'w+')
    OutPath = os.path.join(outpath, '5.stats')
    if not os.path.exists(OutPath):
        os.mkdir(OutPath)
    clone = outpath+'/4.Annotation/'+ob.name+'_R12_atleast-2_db-pass_FUNCTIONAL-T_clone-pass.tab'
    out.write(BinPath+'/Race/Statistic/MakeStatRace.py '+clone+' '+ob.name+' '+OutPath+'\n')
    out.write(BinPath+'/Race/Statistic/QcPlot.py '+outpath+'/2.QC '+ob.name+' '+OutPath+'\n')
    out.write(BinPath+'/Race/Statistic/StatPlotRace.py PlotVDJ '+OutPath+' '+ob.name+'\n')
    out.write(BinPath+'/Race/Statistic/StatPlotRace.py PlotVJComb '+OutPath+' '+ob.name+'\n')
    out.write(BinPath+'/Race/Statistic/MakeFinalRace.py '+outpath+' '+ob.name+' '+ob.fastq+'\n')
    out.close()

def PlotMulti(BinPath, InPath, OutPath):
    path_stat = glob(InPath+'/analysis/*/*/5.stats')
    path_clone = glob(InPath+'/analysis/*/*/5.stats/*.clonetype.filter.txt')
    out = open(os.path.join(InPath, 'Multi.sh'), 'w+')
    out.write(BinPath+'/Race/Statistic/StatPlotRace.py PlotCDR3Bar '+\
              ','.join(path_stat)+' a '+OutPath+'\n')
    out.write(BinPath+'/Race/Statistic/StatPlotRace.py PlotCDR3Bar '+\
              ','.join(path_stat)+' n '+OutPath+'\n')
    out.write(BinPath+'/Race/Statistic/VennPlotRace.py n '+\
              ' '.join(path_clone)+' '+OutPath+'\n')
    out.write(BinPath+'/Race/Statistic/VennPlotRace.py a '+\
              ' '.join(path_clone)+' '+OutPath+'\n')
    out.write(BinPath+'/Race/Statistic/CountMixRace.py '+InPath+' '+OutPath+'\n')
    if len(path_stat) >2:
        out.write(BinPath+'/Race/Statistic/MixAnalysisRace.py '+InPath+'\n')
    out.close()

def PlotCorr(BinPath, gp1, gp2, InPath, OutPath):
    gp1_path = '/'.join([InPath, 'analysis', gp1])
    gp2_path = '/'.join([InPath, 'analysis', gp2])
    gn1 = re.split('/', gp1)[-1]
    gn2 = re.split('/', gp2)[-1]
    out = open(os.path.join(InPath, 'Corr.sh'), 'a+')
    out.write(BinPath+'/Race/Statistic/CompareRace.py VGene '+\
             gp1_path+'/5.stats/'+gn1+'.V.stat '+\
             gp2_path+'/5.stats/'+gn2+'.V.stat '+OutPath+'\n')
    out.write(BinPath+'/Race/Statistic/CompareRace.py VJ '+\
              gp1_path+'/5.stats/'+gn1+'.VJCom.stat '+\
              gp2_path+'/5.stats/'+gn2+'.VJCom.stat '+OutPath+'\n')
    out.write(BinPath+'/Race/Statistic/CompareRace.py VDJ '+\
              gp1_path+'/5.stats/'+gn1+'.VDJCom.stat '+\
              gp2_path+'/5.stats/'+gn2+'.VDJCom.stat '+OutPath+'\n')
    out.write(BinPath+'/Race/Statistic/CompareRace.py VFamily '+\
              gp1_path+'/5.stats/'+gn1+'.VFamily.stat '+\
              gp2_path+'/5.stats/'+gn2+'.VFamily.stat '+OutPath+'\n')
    out.close()

def DivAndAbun(BinPath, InPath, OutPath):
    out = open(os.path.join(InPath, 'DivAndAbun.sh'), 'w+')
    out.write(BinPath+'/Race/Statistic/Tab2Alakazam.py '+InPath+' '+OutPath+'\n')
    out.write(BinPath+'/Rscript '+BinPath+'/Race/Statistic/DivAndAbun.R '+\
            os.path.join(OutPath, 'Alakazam.tab')+\
            ' '+OutPath+'/Abundance.pdf '+\
             OutPath+'/Diversity.pdf'+'\n')
    out.write(' '.join(['convert', OutPath+'/Abundance.pdf', \
                        OutPath+'/Abundance.png'])+'\n')
    out.write(' '.join(['convert', OutPath+'/Diversity.pdf', \
                        OutPath+'/Diversity.png'])+'\n')
    out.write(BinPath+'/Race/Statistic/GetDiversityIndex.py '+InPath)
    out.close()

def MakeReport(BinPath, InPath, tp, project, als, comparegroup):
#    gn1 = re.split('/', gp1)[-1]
#    gn2 = re.split('/', gp2)[-1]
    out = open(os.path.join(InPath, 'report.sh'), 'w+')
    outpath = os.path.join(InPath, 'Report')
    out.write(BinPath+'/Race/MakeReportRace.py '+InPath+'/analysis '+outpath+\
              ' '+str(tp)+' '+project+' '+als+' '+comparegroup)
    out.close()

def ArgparseLine():
    parser = argparse.ArgumentParser(description="ReqSeq pipeline")
    parser.add_argument('--type',help="the type of the analysis",\
                         choices=['IGH', 'TRA', 'TRB', 'IGK', 'IGL'],\
                        required=True)
    parser.add_argument('--specie',help="the specie",\
                        choices=['human', 'mouse', 'rat']  ,required=True)
    parser.add_argument('--list',help="the input fastq list", required=True)
    parser.add_argument('--outdir',help="the output dir", required=True)
    parser.add_argument('--project',help="the NGS number", required=True)
    parser.add_argument('--datatype',\
                        choices=['illumina','solexa','sra','454','presto'],\
                                 help="the fastq type", required=True)
    parser.add_argument('--compare', choices=['0', '1'],\
                        default=0, help="whether compare group", required=True)
    parser.add_argument('--group',help="the compare group, for example A1,A2,A3:B1,B2,B3", required=True)
    parser.add_argument('--run', choices=['0', '1'],\
                        default=1, help="whether run shell right now", required=True)
    argv=vars(parser.parse_args())
    return argv



def main():
    argv = ArgparseLine()
    BinPath = os.path.split(os.path.realpath(__file__))[0]
    outdir = argv['outdir']
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    AnalysisDir = os.path.join(outdir, 'analysis')
    if not os.path.exists(AnalysisDir):
        os.mkdir(AnalysisDir)
    bsub = BinPath+'/bsub.sh'
    bs = BinPath+'/bsub2.sh'
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
            allshell = open(os.path.join(SingleDir, 'all.sh'), 'w+')
            os.chdir(SingleDir)
            allshell.write('echo ========Start CutPrimer at : `date`========'+'\n')
            CutPrimer(BinPath, ob, ShellDir, SingleDir)
            allshell.write(' '.join([bs, os.path.join(ShellDir, '1.CutPrimer.sh'), \
                                    '1', os.path.join(ShellDir, '1.CutPrimer.sh')])+'\n')
            allshell.write('echo ========End CutPrimer at : `date`========'+'\n'+\
                           'echo ========Start QC at : `date`========'+'\n')
            QC(BinPath, ob, ShellDir, SingleDir)
            allshell.write(' '.join([bs, os.path.join(ShellDir,'2.QC.sh'),\
                                     '5', os.path.join(ShellDir,'2.QC.sh')])+'\n')
            allshell.write('echo ========End QC at : `date`========'+'\n'+\
                          ' echo ========Start GetSeq at : `date`========'+'\n')
            GetSeq(BinPath, ob, ShellDir, SingleDir)
            allshell.write(' '.join([bs, os.path.join(ShellDir, '3.GetSeq.sh'),\
                                    '5', os.path.join(ShellDir, '3.GetSeq.sh')])+'\n')
            allshell.write('echo ========End GetSeq at : `date`========'+'\n'+\
                           'echo ========Start Annotation at : `date`========'+'\n')
            Annotation(BinPath, ob, argv['type'], argv['specie'], ShellDir, SingleDir)
            allshell.write(' '.join([bs, os.path.join(ShellDir, '4.Annotation.sh'),\
                                     '4', os.path.join(ShellDir, '4.Annotation.sh')])+'\n')
            allshell.write('echo ========End Annotation at : `date`========'+'\n'+\
                           'echo ========Start MakeSingle at : `date`========'+'\n')
            MakeSingle(BinPath, ob, ShellDir, SingleDir)
            allshell.write(' '.join([bs, os.path.join(ShellDir, '5.Single.sh'),\
                                     '1', os.path.join(ShellDir, '5.Single.sh')])+'\n')
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
        CompareShell.write('echo ========End Compare at : `date`========'+'\n')
        CompareShell.close()
        if int(argv['run']):
            os.system('nohup sh Compare.sh&')
    if int(argv['compare']):
        tp = 1
        CompareGroup = argv['group']
    else:
        tp = 0
        CompareGroup = 'None'
    ReportShell = open(os.path.join(outdir, 'Report.sh'), 'w+')
    ReportShell.write('echo ========Start Report at : `date`========'+'\n')
    MakeReport(BinPath, outdir, tp, argv['project'], argv['type'], CompareGroup)
    ReportShell.write(' '.join([bs, os.path.join(outdir,\
                        'report.sh'), '1', 'report'])+'\n')
    ReportShell.write('echo ========End Report at : `date`========'+'\n'+\
                          'echo ALL JOBS DONE')
    CompareShell.close()
    if int(argv['run']):
        os.system('nohup sh Reprot.sh&')


if __name__ == '__main__':
    main()

