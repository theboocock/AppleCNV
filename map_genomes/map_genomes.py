#!/usr/bin/python3
#
# Script to run a full BWA bioinformatics pipeline for the apple_read_data
#
#

from parallel import *
import os

commands = []
cores = 2

bwa_path = '/Volumes/BiochemXsan/Staff_Users/jamesboocock/bin/bwa-0.7.5a/bwa'
directory = '/Volumes/merrimanlab/Documents/James/new_apple_data/ReSequencing/dual_read'
reference_genome = '/Volumes/merrimanlab/Documents/James'

for item in os.listdir(directory):
    if os.path.isfile(item):
