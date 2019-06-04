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
    parser.add_argument('--f1',help="the input fastq1", required=True)
    parser.add_argument('--f2',help="the input fastq2", required=True)
    parser.add_argument('--type',help="the type of the analysis",\
                        choices=['IGH', 'TRA', 'TRB', 'IGK', 'IGL'], required=True)
    parser.add_argument('--name',help="the output name", required=True)
    parser.add_argument('--specie',help="the specie",
                        choices=['human', 'mouse', 'rat', 'rabbit', \
                                'rhesus_monkey']  ,required=True)
    argv=vars(parser.parse_args())
    return argv

def MakeQcJob():
    argv = ArgparseLine()
    bin_path = '/ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/bin'
    out = open('Qc.job', 'w+')
    ob0 = Job('PairSeq')
    list_sched0 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=3g,p=1']
    list_arg0 = ['-1 '+argv['f1'], '-2 '+argv['f2'], '--coord presto']
    out.write(ob0.job(list_sched0, bin_path+'/PairSeq.py', list_arg0)+'\n\n')
    ob01 = Job('TrimHeader1')
    list_sched01 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=1g,p=1']
    list_arg01 = [argv['name']+'_R1_pair-pass.fastq',]
    out.write(ob01.job(list_sched01, bin_path+'/TrimHeader.py', list_arg01)+'\n\n')
    ob02 = Job('TrimHeader2')
    list_arg02 = [argv['name']+'_R2_pair-pass.fastq',]
    out.write(ob02.job(list_sched01, bin_path+'/TrimHeader.py', list_arg02)+'\n\n')
    out.write('order TrimHeader1 after PairSeq'+'\n'+\
             'order TrimHeader2 after PairSeq'+'\n\n')
    ob1 =Job('AssemblePairs')
    list_sched1 = ['-V', '-cwd', '-P', 'mem6', '-q', 'mem6.q', '-l', 'vf=20g,p=5']
    list_arg1 = ['align',\
                '-1 '+argv['name']+'_R1_pair-pass_trim.fastq',\
                 '-2 '+argv['name']+'_R2_pair-pass_trim.fastq',\
                 '--coord presto','--rc tail',\
                 '--outname '+argv['name']+'_R12', '--log AP.log']
    out.write(ob1.job(list_sched1, bin_path+'/AssemblePairs.py', list_arg1)+'\n\n')
    out.write('order AssemblePairs after TrimHeader1'+'\n'+\
             'order AssemblePairs after TrimHeader2'+'\n\n')
    ob2 = Job('FilterSeq')
    list_arg2 = ['quality', '-s '+argv['name']+'_R12_assemble-pass.fastq',\
                 '-q 20', '--outname '+argv['name']+'_R12', '--log QC.log']
    out.write(ob2.job(list_sched1, bin_path+'/FilterSeq.py', list_arg2)+'\n\n')
    out.write('order FilterSeq after AssemblePairs'+'\n\n')
    ob3 = Job('CollapseSeq')
    list_sched2 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=1g,p=1']
    list_arg3 = ['-s '+argv['name']+'_R12_quality-pass.fastq',\
                 '-n 20', '--inner', '--outname '+argv['name']+'_R12']
    out.write(ob3.job(list_sched2, bin_path+'/CollapseSeq.py', list_arg3)+'\n\n')
    out.write('order CollapseSeq after FilterSeq'+'\n\n')
    ob4 = Job('SplitSeq')
    list_arg4 = ['group', '-s '+argv['name']+'_R12_collapse-unique.fastq',\
                 '-f DUPCOUNT', '--num 2', '--outname '+argv['name']+'_R12']
    out.write(ob4.job(list_sched2, bin_path+'/SplitSeq.py', list_arg4)+'\n\n')
    out.write('order SplitSeq after CollapseSeq'+'\n\n')
    ob5 = Job('ParseHeaders')
    list_arg5 = ['table',\
                 '-s '+argv['name']+'_R12_atleast-2.fastq',\
                 '-f ID DUPCOUNT']
    out.write(ob5.job(list_sched2, bin_path+'/ParseHeaders.py', list_arg5)+'\n\n')
    out.write('order ParseHeaders after SplitSeq'+'\n\n')
    out.write('log_dir log')
    out.close()

def MakeAsJob():
    argv = ArgparseLine()
    bin_path = '/ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/bin/ChangeO'
    ref_path = '/ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/RefData/'
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
                 '-r '+ref_path+argv['specie']+'/'+argv['type'],\
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
    if argv['type'] in ['IGH', 'IGK', 'IGL']:
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
                    '-r '+ref_path+argv['specie']+'/'+argv['type'],\
                    '-g dmask', '--cloned']
        out.write(ob5.job(list_sched2, bin_path+'/CreateGermlines.py',\
                          list_arg5)+'\n\n')
        out.write('order CreateGermlines after DefineClones'+'\n\n')
    elif argv['type'] in ['TRB', 'TRA']:
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
