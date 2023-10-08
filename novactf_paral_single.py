#!/usr/bin/env python3
# 2023/10 HB, McGill University
# Usage: python novactf_paral.py script_template ts_name no_defocus_file
# No defocus file = last number (start from 0)
# Template file use #ts for ts_name and #n for the number of defocus file
# Can deal with .script file with multiple lines
# Only serve in case things doesn't work

import sys,os,time
from datetime import datetime

import subprocess, multiprocessing


def print_usage():
	print("python novactf_paral_single.py script_template ts_name no_defocus_file no_proc")
	print("e.g.: novactf_paral_single.py step4_ctfcorr.script 0344_dose-filt 40 10");
	sys.exit(0)

def execute_group(cmd_list):
	""" Function to execute command as a group """
	for cmd in cmd_list:
		print(f'start {cmd}', datetime.now())
		#subprocess.call(cmd,shell=True)	

if __name__ == "__main__":

	if len(sys.argv) < 4:
		print_usage()

	ts_name = sys.argv[2]
	no_files = int(sys.argv[3])
	threads = int(sys.argv[4])

	with open(sys.argv[1], 'r') as f:
	   	scripts = [line.strip() for line in f.readlines()]
	
	cmds = []
	for id in range(no_files + 1):
		cmd_list = []
		# Go through all command
		for script in scripts:
			if script.isspace() < 1:
				cmd_list.append(script.replace('#n', str(id)).replace('#ts', ts_name))				
		cmds.append(cmd_list)

	with multiprocessing.Pool(processes=threads) as pool:
		results = pool.map(execute_group, cmds)

	


	

	

	
	


