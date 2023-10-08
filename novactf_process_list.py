#!/usr/bin/env python3
# 2023/10 HB, McGill University
# Usage: python novactf_process_list.py tomolist no_proc
# Use novactf to process a list of tomogram stack
# Require novactf_paral_single.py
# Directory structure
# ProjDir
# ------->script templates (step1 to step 5)
# ------->tomolist file
# ------->Tilt series folder TS_001, TS_002 etc.
#
# Tomolist file format
# 	TS_001/TS_001_dose-filt.st
#	TS_010/TS_010_dose-filt.st
#
# In principal, you need .xf file, tilt file & xtilt file and ctffind4 defocus file name defocus_file.txt
# NOTE: the reconstruction step is not parallel this way but it is safer than writing many huge files at the same time

import sys, os, time, subprocess
script_dir=os.path.dirname(os.path.realpath(__file__))
from datetime import datetime



def print_usage():
	print("python novactf_process_list.py tomolist no_proc")
	print("e.g.: novactf_process_list.py tomolist.txt 10")
	sys.exit(0)
	
def execute(cmd):
	print(f'{cmd}')
	return subprocess.call(cmd,shell=True)
	
	
def main():
	if len(sys.argv) < 3:
		print_usage()
		
	no_proc = int(sys.argv[2])

	with open(sys.argv[1], 'r') as input_list:
	    tomo_list = [line.strip() for line in input_list.readlines()]

	currdir = os.getcwd()
	
	for tomo in tomo_list:
		if not os.path.exists(tomo):
			print(f"Error: File '{tomo}' not found.")
			continue

		tspath = os.path.dirname(tomo)
		tsname, tomoxt = os.path.splitext(os.path.basename(tomo))
		
		print('#########################')
		print(f'Processing {tsname}')
		print('#########################')
		
		os.chdir(tspath)
		
		# Generate defocus file
		cmd1 = f'python {script_dir}/novactf_paral_auto.py ../step1_gendeffile.script {tsname} 1'
		execute(cmd1)

		#ctf correction
		cmd2 = f'python {script_dir}/novactf_paral_auto.py ../step2_ctfcorr.script {tsname} {no_proc}'
		execute(cmd2)

		#Align stack
		cmd3 = f'python {script_dir}/novactf_paral_auto.py ../step3_align_flip_stack.script {tsname} {no_proc}'
		execute(cmd3)
		
		#Filter
		cmd4 = f'python {script_dir}/novactf_paral_auto.py ../step4_filter_proj.script {tsname} {no_proc}'
		execute(cmd4)

		# Reconstruction
		cmd5 = f'python {script_dir}/novactf_paral_auto.py ../step5_recon.script {tsname} {no_proc}'
		execute(cmd5)
		
		# Clean
		cmd6 = f'python {script_dir}/novactf_paral_auto.py ../step6_clean.script {tsname} {no_proc}'
		execute(cmd6)
		
		# Done
		print(f'Done processing {tsname}')
		
		
		os.chdir(currdir)

if __name__ == "__main__":
    main()
	

