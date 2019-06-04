#!/ifs/TJPROJ3/DENOVO/lixuefei/soft/anaconda2/bin/python2

import argparse
import re

class Job(object):
    '''
    sjm job object
    '''
    def __init__(self, string_in):
        self.name = string_in
    
    def sched(self, list_in):
        '''
        the sched_options line
        '''
        return 'sched_options '+' '.join(list_in)

    def script(self, string_in):
        return string_in

    def script_arg(self, list_in):
        return '\n\t\t\t'.join(list_in)

    def job(self, list_sched, script_str, list_arg):
        if list_arg :
            return 'job_begin'+'\n\t'+'name '+self.name+'\n\t'+\
                    self.sched(list_sched)+'\n\t'+\
                    'cmd_begin\n\t\t'+self.script(script_str)+'\n\t\t\t'+\
                    self.script_arg(list_arg)+'\n\tcmd_end\njob_end'


def ArgparseLine():
    parser = argparse.ArgumentParser(description="ReqSeq pipeline")
#    parser.add_argument('--outjob',help="the output job", required=True)
    parser.add_argument('--f1',help="the input fastq1", required=True)
    parser.add_argument('--f2',help="the input fastq2", required=True)
    parser.add_argument('--umi',help="the umi fastq", required=True)
    parser.add_argument('--type',help="the type of the analysis",\
                        choices=['IG', 'TR'], required=True)
#    parser.add_argument('--ref',help="the reference sequence", required=True)
    parser.add_argument('--name',help="the output name", required=True)
    parser.add_argument('--specie',help="the specie", 
                        choices=['human', 'mouse', 'rat', 'rabbit', \
                                'rhesus_monkey']  ,required=True)
    argv=vars(parser.parse_args())
    return argv

def MakeQcJob():
    argv = ArgparseLine()
    bin_path = '/ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/bin'
    ref = '/ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/RefData/regions.fa'
    out = open('Qc.job', 'w+')
    ob1 = Job('FilterSeq1')
    list_arg1 = ['quality', '-s '+argv['f1'], '-q 20',\
                   '--outname '+argv['name']+'_R1', '--log QC1.log']
    list_sched1 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=5g,p=5']
    out.write(ob1.job(list_sched1, bin_path+'/FilterSeq.py', list_arg1)+'\n\n')
    ob2 = Job('FilterSeq2')
    list_arg2 = ['quality', '-s '+argv['f2'], '-q 20',\
                 '--outname '+argv['name']+'_R2', '--log QC2.log']
    out.write(ob2.job(list_sched1, bin_path+'/FilterSeq.py', list_arg2)+'\n\n')
    ob30 = Job('PairedFq')
    list_sched30 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=5g,p=1']
    list_arg30 = ['--f1 '+argv['name']+'_R1_quality-pass.fastq',\
                  '--f2 '+argv['name']+'_R2_quality-pass.fastq']
    out.write(ob30.job(list_sched30, bin_path+'/PairedFq.py', list_arg30)+'\n\n')
    out.write('order PairedFq after FilterSeq1'+'\n'+\
              'order PairedFq after FilterSeq2'+'\n\n')
    ob31 = Job('AlignRead')
    list_sched31 = ['-V', '-cwd', '-P', 'mem11', '-q', 'mem11.q', '-l',\
                   'vf=30g,p=10']
    list_arg31 = ['--ref '+ ref, '--f1 '+\
                  argv['name']+'_R1_quality-pass_pairedfq-pass.fastq', '--f2 '+\
                 argv['name']+'_R2_quality-pass_pairedfq-pass.fastq', '--out '+\
                  argv['name']+'_align.sam']
    out.write(ob31.job(list_sched31, bin_path+'/AlignRead.py', list_arg31)+'\n\n')
    out.write('order AlignRead after PairedFq'+'\n\n')
    ob32 = Job('GroupUMI')
    list_sched32 = ['-V', '-cwd', '-P', 'mem11', '-q', 'mem11.q', '-l',\
                    'vf=30g,p=30']
    list_arg32 = ['--umi '+argv['umi'], '--sam '+argv['name']+'_align.sam',\
                  '--type '+argv['type'], '--out '+argv['name']+'_umi.json']
    out.write(ob32.job(list_sched32, bin_path+'/GroupUMI.py', list_arg32)+'\n\n')
    out.write('order GroupUMI after AlignRead'+'\n\n')
    ob33 = Job('PairedSeq')
    list_sched2 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=5g,p=1']
    list_arg33 = ['--f1 '+argv['name']+'_R1_quality-pass_pairedfq-pass.fastq', '--f2 '+\
                argv['name']+'_R2_quality-pass_pairedfq-pass.fastq', '--umi '+\
                 argv['name']+'_umi.json']
    out.write(ob33.job(list_sched2, bin_path+'/PairedSeq.py', list_arg33)+'\n\n')
    out.write('order PairedSeq after GroupUMI'+'\n\n')
    ob4 = Job('AlignSets1')
    list_sched4 = ['-V', '-cwd', '-P', 'mem11', '-q', 'mem11.q', '-l',\
                   'vf=60G,p=10']
    list_arg4 = ['muscle', '-s '+argv['name']+'_R1_quality-pass_pairedfq-pass_paired-pass.fastq',\
                 '--exec /ifs/TJPROJ3/DENOVO/lixuefei/soft/bin/muscle',\
                '--outname '+argv['name']+'_R1', '--log AS1.log']
    out.write(ob4.job(list_sched4, bin_path+'/AlignSets.py', list_arg4)+'\n\n')
    ob5 = Job('AlignSets2')
    list_arg5 = ['muscle', '-s '+argv['name']+'_R2_quality-pass_pairedfq-pass_paired-pass.fastq',\
                 '--exec /ifs/TJPROJ3/DENOVO/lixuefei/soft/bin/muscle',\
                 '--outname '+argv['name']+'_R2', '--log AS2.log']
    out.write(ob5.job(list_sched4, bin_path+'/AlignSets.py', list_arg5)+'\n\n')
    out.write('order AlignSets1 after PairedSeq'+'\n'+\
              'order AlignSets2 after PairedSeq '+'\n\n')
    ob6 = Job('BuildConsensus1')
    list_sched6 = ['-V', '-cwd', '-P', 'mem11', '-q', 'mem11.q', '-l',\
                   'vf=20G,p=10']
    list_arg6 = ['-s '+argv['name']+'_R1_align-pass.fastq', '--bf BARCODE',\
                '--maxerror 0.1', '--maxgap 0.5',\
                 '--outname '+argv['name']+'_R1', '--log BC1.log']
    out.write(ob6.job(list_sched6, bin_path+'/BuildConsensus.py', list_arg6)+'\n\n')
    ob7 = Job('BuildConsensus2')
    list_arg7 = ['-s '+argv['name']+'_R2_align-pass.fastq', '--bf BARCODE',\
                 '--maxerror 0.1', '--maxgap 0.5',\
                 '--outname '+argv['name']+'_R2', '--log BC2.log']
    out.write(ob7.job(list_sched6, bin_path+'/BuildConsensus.py', list_arg7)+'\n\n')
    out.write('order BuildConsensus1 after AlignSets1'+'\n'+\
              'order BuildConsensus2 after AlignSets2'+'\n\n')
    ob8 = Job('PairSeq')
    list_sched8 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=1g,p=1']
    list_arg8 = ['-1 '+argv['name']+'_R1_consensus-pass.fastq',\
                '-2 '+argv['name']+'_R2_consensus-pass.fastq',\
                '--coord presto']
    out.write(ob8.job(list_sched8, bin_path+'/PairSeq.py', list_arg8)+'\n\n')
    out.write('order PairSeq after BuildConsensus1'+'\n'+\
             'order PairSeq after BuildConsensus2'+'\n\n')
    ob9 =Job('AssemblePairs')
    list_arg9 = ['align',\
                '-1 '+argv['name']+'_R1_consensus-pass_pair-pass.fastq',\
                '-2 '+argv['name']+'_R2_consensus-pass_pair-pass.fastq',\
                '--coord presto', '--rc tail', '--1f CONSCOUNT',\
                '--2f CONSCOUNT', '--outname '+argv['name']+'_R12',\
                '--log AP.log']
    out.write(ob9.job(list_sched6, bin_path+'/AssemblePairs.py', list_arg9)+'\n\n')
    out.write('order AssemblePairs after PairSeq'+'\n\n')
    ob10 =Job('ParseHeaders1')
    list_arg10 = ['collapse', '-s '+argv['name']+'_R12_assemble-pass.fastq',\
                 '-f CONSCOUNT', '--act min']
    out.write(ob10.job(list_sched8, bin_path+'/ParseHeaders.py', list_arg10)+'\n\n')
    out.write('order ParseHeaders1 after AssemblePairs'+'\n\n')
    ob11 = Job('CollapseSeq')
    list_arg11 = ['-s '+argv['name']+'_R12_assemble-pass_reheader.fastq',\
                 '-n 20', '--inner', '--cf CONSCOUNT', '--act sum',\
                 '--outname '+argv['name']+'_R12']
    out.write(ob11.job(list_sched8, bin_path+'/CollapseSeq.py', list_arg11)+'\n\n')
    out.write('order CollapseSeq after ParseHeaders1'+'\n\n')
    ob12 = Job('SplitSeq')
    list_arg12 = ['group', '-s '+argv['name']+'_R12_collapse-unique.fastq',\
                 '-f CONSCOUNT', '--num 2',\
                  '--outname '+argv['name']+'_R12']
    out.write(ob12.job(list_sched8, bin_path+'/SplitSeq.py', list_arg12)+'\n\n')
    out.write('order SplitSeq after CollapseSeq'+'\n\n')
    ob13 = Job('ParseHeaders2')
    list_arg13 = ['table',\
                 '-s '+argv['name']+'_R12_atleast-2.fastq',\
                 '-f ID CONSCOUNT DUPCOUNT']
    out.write(ob13.job(list_sched8, bin_path+'/ParseHeaders.py', list_arg13)+'\n\n')
    out.write('order ParseHeaders2 after SplitSeq'+'\n\n')
    out.write('log_dir log')
    out.close()

def MakeAsJob():
    argv = ArgparseLine()
    bin_path = '/ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/bin/ChangeO'
    out = open('Analysis.job', 'w+')
    ob1 = Job('HandleIgBlast')
    list_arg1 = ['--fq '+argv['name']+'_R12_atleast-2.fastq', \
                '--specie '+argv['specie'], '--type '+argv['type']]
    list_sched1 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=3g,p=5']
    out.write(ob1.job(list_sched1, bin_path+'/HandleIgBlast.py',\
                       list_arg1)+'\n\n')
    ob2 = Job('MakeDb')
    list_sched2 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=1g,p=1']
    list_arg2 = ['igblast','-i '+argv['name']+'_R12_atleast-2.fmt7', \
                '-s '+argv['name']+'_R12_atleast-2.fasta', \
                 '-r /ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/RefData/human/Ig/',\
                '--regions', '--scores']
    out.write(ob2.job(list_sched2, bin_path+'/MakeDb.py',\
                      list_arg2)+'\n\n')
    out.write('order MakeDb after HandleIgBlast'+'\n\n')
    ob3 = Job('ParseDb')
    list_arg3 = ['split', '-d '+argv['name']+'_R12_atleast-2_db-pass.tab', \
                '-f FUNCTIONAL']
    out.write(ob3.job(list_sched2, bin_path+'/ParseDb.py',\
                      list_arg3)+'\n\n')
    out.write('order ParseDb after MakeDb'+'\n\n')
    if argv['type'] == 'IG':
        ob4 = Job('DefineClones')
        list_arg4 = ['bygroup', \
                     '-d '+argv['name']+'_R12_atleast-2_db-pass_FUNCTIONAL-T.tab',\
                    '--act set', '--model ham', '--sym min', \
                    '--norm len', '--dist 0.16']
        out.write(ob4.job(list_sched1, bin_path+'/DefineClones.py',\
                          list_arg4)+'\n\n')
        out.write('order DefineClones after ParseDb'+'\n\n')
        ob5 = Job('CreateGermlines')
        list_arg5 = ['-d '+argv['name']+'_R12_atleast-2_db-pass_FUNCTIONAL-T_clone-pass.tab',\
                    '-r /ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/RefData/human/Ig/',\
                    '-g dmask', '--cloned']
        out.write(ob5.job(list_sched2, bin_path+'/CreateGermlines.py',\
                          list_arg5)+'\n\n')
        out.write('order CreateGermlines after DefineClones'+'\n\n')
    elif argv['type'] == 'TR':
        ob4 = Job('HandleTCR')
        list_arg4 = ['--in '+argv['name']+'_R12_atleast-2_db-pass_FUNCTIONAL-T.tab',]
        out.write(ob4.job(list_sched2, bin_path+'/HandleTCR.py',\
                          list_arg4)+'\n\n')
        out.write('order HandleTCR after ParseDb'+'\n\n')
    out.write('log_dir log')
    out.close()

def main():
    MakeQcJob()
    MakeAsJob()


if __name__ == '__main__':
    main()