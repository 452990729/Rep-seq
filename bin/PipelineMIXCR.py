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
                        choices=['hsa', 'mmu', 'rat']  ,required=True)
    argv=vars(parser.parse_args())
    return argv

def MakeQcJob():
    argv = ArgparseLine()
    bin_path = '/ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/bin'
    Mixcr_path = \
    '/ifs/TJPROJ3/DENOVO/lixuefei/novo/bin/Group/bin/Mixcr/mixcr-2.1.5'
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
    list_sched2 = ['-V', '-cwd', '-q', 'all.q,novo.q', '-l', 'vf=2g,p=1']
    ob3 = Job('PairSeq')
    list_arg3 = ['-1 '+argv['name']+'_R1_quality-pass.fastq',\
                 '-2 '+argv['name']+'_R2_quality-pass.fastq',\
                 '--coord illumina']
    out.write(ob3.job(list_sched2, bin_path+'/PairSeq.py',\
                       list_arg3)+'\n\n')
    out.write('order PairSeq after FilterSeq1'+'\n'+\
             'order PairSeq after FilterSeq2'+'\n\n')
    ob4 = Job('Align')
    list_arg4 = ['align', '-r align.txt', '-c '+argv['type'],\
                 '-s '+argv['specie'], '-t 5 --library imgt',\
                argv['name']+'_R1_quality-pass_pair-pass.fastq',\
                argv['name']+'_R2_quality-pass_pair-pass.fastq',\
                'alignments.vdjca']
    list_sched4 = ['-V', '-cwd', '-P', 'mem11', '-q', 'mem11.q', '-l',\
                    'vf=20G,p=5']
    out.write(ob4.job(list_sched4, Mixcr_path+'/mixcr',\
                      list_arg4)+'\n\n')
    out.write('order Align after PairSeq'+'\n\n')
    ob5 = Job('Assemble')
    list_arg5 = ['assemble', '-r assemble.txt -t 5', 'alignments.vdjca',\
                'clones.clns']
    out.write(ob5.job(list_sched4, Mixcr_path+'/mixcr',\
                      list_arg5)+'\n\n')
    out.write('order Assemble after Align'+'\n\n')
    ob6 = Job('ExportClones')
    list_arg6 = ['exportClones', '-cloneId -count -fraction ',\
                 '-vGene -dGene -jGene -vHitScore -dHitScore -jHitScore ',\
                 '-vFamily -dFamily -jFamily -nFeature CDR3 -aaFeature CDR3 ',\
                 'clones.clns', argv['name']+'.clones.txt']
    out.write(ob6.job(list_sched4, Mixcr_path+'/mixcr',\
                      list_arg6)+'\n\n')
    out.write('order ExportClones after Assemble'+'\n\n')
    ob7 = Job('MixcrFliter')
    list_arg7 = [argv['name']+'.clones.txt',]
    out.write(ob7.job(list_sched2, bin_path+'/Mixcr/MixcrFliter.py',\
                     list_arg7)+'\n\n')
    out.write('order MixcrFliter after ExportClones'+'\n\n')
    ob8 = Job('MakeStatMixcr')
    list_arg8 = [argv['name']+'.CloneFilter.txt', argv['name']]
    out.write(ob8.job(list_sched2, bin_path+'/Statistic/MakeStatMixcr.py',\
                     list_arg8)+'\n\n')
    out.write('order MakeStatMixcr after MixcrFliter'+'\n\n')
    ob9 = Job('Mixcr2Alakazam')
    list_arg9 = [argv['name']+'.CloneFilter.txt']
    out.write(ob9.job(list_sched2, bin_path+'/Mixcr/Mixcr2Alakazam.py',\
                     list_arg9)+'\n\n')
    out.write('order Mixcr2Alakazam after MixcrFliter'+'\n\n')
    out.write('log_dir log')
    out.close()

def main():
    MakeQcJob()


if __name__ == '__main__':
    main()
