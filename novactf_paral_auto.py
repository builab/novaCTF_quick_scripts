#!/usr/bin/env python3
# 2023/10 HB, McGill University
# Usage: python novactf_paral_auto.py script_template ts_name no_proc
# No defocus file = last number (start from 0)
# Template file use #ts for ts_name and #n for the number of defocus file
# Can deal with multiple line .script file but they must be same #n or not
# Automatic find out about no. of defocus file (must be defocus_file.txt)
# Better than novactf_paral_single.py

import sys
import os
from datetime import datetime
import subprocess
import multiprocessing

def print_usage():
    print("python novactf_paral_auto.py script_template ts_name no_proc")
    print("e.g.: novactf_paral_auto.py step4_ctfcorr.script 0344_dose-filt 10")
    sys.exit(0)

def execute_group(cmd_list):
    """ Function to execute command as a group """
    for cmd in cmd_list:
        print(cmd)
        subprocess.call(cmd, shell=True) 

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()

	if not os.path.exists('defocus_file.txt'):
		print(f"Error: File defocus_file.txt not found. The ctffind4 defocus file must be named defocus_file.txt.")
		sys.exit(0)
		
    ts_name = sys.argv[2]
    threads = int(sys.argv[3])

    # Determine the highest defocus file number assume number never exceed 100
    no_files = 0
    for i in range(100):
        if os.path.exists(f'defocus_file.txt_{i}'):
            no_files = no_files + 1

    print(f'Found {no_files} defocus file')

    with open(sys.argv[1], 'r') as f:
        scripts = [line.strip() for line in f.readlines()]

    cmds = []
    for id in range(no_files):
        cmd_list = []
        # Go through all command
        for script in scripts:
            if script.strip() and ('#n' in script or id == 0):
                cmd_list.append(script.replace('#n', str(id)).replace('#ts', ts_name))
        cmds.append(cmd_list)

    with multiprocessing.Pool(processes=threads) as pool:
        pool.map(execute_group, cmds)
