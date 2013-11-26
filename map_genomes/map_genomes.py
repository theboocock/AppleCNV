#!/usr/bin/python3
#
# Script to run a full BWA bioinformatics pipeline for the apple_read_data
#
#

from parallel import *
import os
import re

commands = []
cores = 2

working_dir = '/mnt/Bioc Merriman Lab/Documents/James/new_apple_data/ReSequencing/new_fifteen'

os.chdir(working_dir)

#bwa_path = '/Volumes/BiochemXsan/Staff_Users/jamesboocock/bin/bwa-0.7.5a/bwa'
#directory = '/Volumes/merrimanlab/Documents/James/new_apple_data/ReSequencing/dual_read'
directory = '/mnt/Bioc Merriman Lab/Documents/James/new_apple_data/ReSequencing/new_fifteen'

bwa = 'bwa'
#reference_genome = '/Volumes/merrimanlab/Documents/James'
# Indexed reference
reference_genome = '/mnt/Bioc Merriman Lab/Documents/James/new_apple_data/Malus_x_domestica.v1.0-primary.pseudo.fa'
for item in os.listdir(directory):
    if(item.endswith(".fastq")): 
        if os.path.isfile(item):
            cmd = []
            cmd.extend(['bwa','aln',reference_genome,item])
            output_name =  os.path.basename(item)
            output_name = output_name.split('.fastq')[0] +'.sai'
            cmd.append(output_name)
            commands.append(cmd)
print(commands)
queue_jobs(commands,cores)
# get all the reads
aligned_fastq = sorted(os.listdir(working_dir))

# read matching 
r_one_match = re.compile(r".*_1.fastq")
r_two_match = re.compile(r".*_2.fastq")
# sai matching 
s_one_match = re.compile(r".*_1.sai")
s_two_match = re.compile(r".*_2.sai")

read_one =  filter(r_one_match.match,aligned_fastq)
read_two =  filter(r_two_match.match,aligned_fastq)

sai_one =  filter(s_one_match.match,aligned_fastq)
sai_two =  filter(s_two_match.match,aligned_fastq)


sampe_commands = []
for rOne, rTwo, saiOne, saiTwo in zip(read_one,read_two,sai_one,sai_two):
    cmd = []
    cmd.extend(['bwa','sampe',reference_genome])
    cmd.extend([saiOne,rOne,saiTwo,rTwo])
    output_name=os.path.basename(rOne)
    output_name=output_name.split('_1.fastq')[0]
    cmd.append(output_name)
    sampe_commands.append(cmd)

print(sampe_commands)


##### SAM TOOLS commands #########





