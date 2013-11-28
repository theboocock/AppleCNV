#!/usr/bin/python
#
# Script to run a full BWA bioinformatics pipeline for the apple_read_data
#
#

from parallel import *
import os
import re

commands = []
cores =10

directory = '/Volumes/merrimanlab/Documents/James/new_apple_data/ReSequencing/new_fifteen'

reference_genome = '/Volumes/merrimanlab/Documents/James/new_apple_data/Malus_x_domestica.v1.0-primary.pseudo.fa'

bwa_path = '/Volumes/BiochemXsan/Staff_Users/jamesboocock/bin/bwa-0.7.5a/bwa'
sam_tools_path = '/Volumes/BiochemXsan/Staff_Users/jamesboocock/bin/samtools'
working_dir = '/Volumes/merrimanlab/Documents/James/new_apple_data/ReSequencing/new_fifteen/alignments'
# read matching 
r_one_match = re.compile(r".*_1.fastq")
r_two_match = re.compile(r".*_2.fastq")
# sai matching 
s_one_match = re.compile(r".*_1.sai")
s_two_match = re.compile(r".*_2.sai")

index_reference = ([bwa_path,'index',reference_genome])
#queue_jobs([Command(index_reference)],cores)


os.chdir(working_dir)
if not (os.path.exists(working_dir)):
    print(working_dir)
    os.mkdir(working_dir)

print(working_dir)
for item in os.listdir(directory):
    if(item.endswith(".fastq")): 
        item = os.path.join(directory,item)
        cmd = []
        cmd.extend([bwa_path,'aln',reference_genome,item])
        output_name =  os.path.basename(item)
        output_name = output_name.split('.fastq')[0] +'.sai'
        commands.append(Command(cmd,output_name))
queue_jobs(commands,cores)
# get all the reads
aligned_fastq = sorted(os.listdir(working_dir))


read_one =  filter(r_one_match.match,aligned_fastq)
read_two =  filter(r_two_match.match,aligned_fastq)

sai_one =  filter(s_one_match.match,aligned_fastq)
sai_two =  filter(s_two_match.match,aligned_fastq)


sampe_commands = []
for rOne, rTwo, saiOne, saiTwo in zip(read_one,read_two,sai_one,sai_two):
    cmd = []
    cmd.extend([bwa_path,'sampe',reference_genome])
    cmd.extend([saiOne,rOne,saiTwo,rTwo])
    output_name=os.path.basename(rOne)
    output_name=output_name.split('_1.fastq')[0] +'.sam'
    sampe_commands.append(Command(cmd,output_name))


queue_jobs(sampe_commands,cores)

##### SAM TOOLS commands #########

sam_to_bam=[]
for item in os.listdir('.'):
    if(item.endswith('.sam')):
        cmd=[]
        cmd.extend([sam_tools_path,'view','-h','-S',item])
        output_name=item.split('.sam')[0]+'.bam'
        sam_to_bam.append(Command(cmd,output_name))
queue_jobs(sam_to_bam,cores)
sort_bam=[]
for item in os.listdir('.'):
    if(item.endswith('.bam')):
        cmd=[]
        cmd.extend([sam_tools_path,'sort',item,item.split('.bam')[0]+ '_sorted'])
        sort_bam.append(Command(cmd))
queue_jobs(sort_bam,cores)
index_bam=[]

for item in os.listdir('.'):
    if(item.endswith('sorted.bam')):
        cmd=[]
        cmd.extend([sam_tools_path,'index',item])
        index_bam.append(Command(cmd))
queue_jobs(index_bam,cores)

