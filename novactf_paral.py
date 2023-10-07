#!/usr/bin/env python3
# 2023/10 HB, McGill University
# Usage: python novactf_paral.py script_template ts_name no_defocus_file
# No defocus file = last number (start from 0)

import sys,os,time
from datetime import datetime

import subprocess, multiprocessing


def print_usage():
	print("python novactf_paral.py script_template ts_name no_defocus_file no_proc")
	print("e.g.: novactf_paral.py ctf_correction.script  0344_dose-filt 40 10");
	sys.exit(0)

def execute(cmd):
	print(f'start {cmd}', datetime.now())
	return subprocess.call(cmd,shell=True)



if __name__ == "__main__":

	if len(sys.argv) < 4:
		print_usage()

	ts_name = sys.argv[2]
	no_files = int(sys.argv[3])
	threads = int(sys.argv[4])

	with open(sys.argv[1]) as f:
   		 script = f.readline().strip('\n')
	
	cmds = []
	for id in range(no_files + 1):
		cmds.append(script.replace('#n', str(id)).replace('#ts', ts_name))

	print(cmds)
	with multiprocessing.Pool(processes=threads) as pool:
		results = pool.map(execute, cmds)

	


	

	

	
	


