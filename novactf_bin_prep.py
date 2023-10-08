#!/usr/bin/env python3
# 2023/10 HB, McGill University
# Usage: python novactf_bin2_prep.py tomolist binFactor no_proc
# Tomolist
# 	TS_001/TS_001_dose-filt.st
#	TS_010/TS_010_dose-filt.st
# In principal, you need .xf file, tilt file & xtilt file.
# Only xf need to adjust the shift, the tlt & xtilt file should be exactly the same.

import sys
import os
import shutil
import subprocess, multiprocessing

def print_usage():
	print("python novactf_bin_prep.py tomolist binfactor no_proc")
	print("e.g.: novactf_bin_prep.py tomolist.txt 2 10")
	sys.exit(0)

def convert_xf(inxf, outxf, bin_factor):
	"""Convert Imod Xf file to new binned one """
	with open(inxf, 'r') as infile:
		lines = infile.readlines()

	with open(outxf, 'w') as outfile:
		for line in lines:
			columns = line.strip().split()
			if len(columns) >= 6:
				output_columns = columns[:4]
				column_5 = float(columns[4]) / 2
				column_6 = float(columns[5]) / 2
				output_columns.append(str(column_5))
				output_columns.append(str(column_6))
				outfile.write('\t'.join(output_columns) + '\n')
	print(f'Output file {outxf} has been created with modified columns.')
	
def process_tomo(tomo, bin_factor):
	if not os.path.exists(tomo):
		print(f"Error: File '{tomo}' not found.")
		return -1

	tspath = os.path.dirname(tomo)
	tsname, tomoxt = os.path.splitext(os.path.basename(tomo))

	# Generate new binned stack
	output_tomo = f'{tspath}/{tsname}_bin{bin_factor}{tomoxt}'
	bincmd = f'newstack -ftreduce {bin_factor} -input {tomo} -output {output_tomo}'
	print(bincmd)
	subprocess.call(bincmd, shell=True)

	# Copy tilt file
	oritlt = f'{tspath}/{tsname}.tlt'
	newtlt = f'{tspath}/{tsname}_bin{bin_factor}.tlt'
	print(f'cp {oritlt} {newtlt}')
	shutil.copy(oritlt, newtlt)

	# Copy xtilt file
	orixtilt = f'{tspath}/{tsname}.xtilt'
	newxtilt = f'{tspath}/{tsname}_bin{bin_factor}.xtilt'
	print(f'cp {orixtilt} {newxtilt}')
	shutil.copy(orixtilt, newxtilt)

	# Convert xf file
	orixf = f'{tspath}/{tsname}.xf'
	newxf = f'{tspath}/{tsname}_bin{bin_factor}.xf'
	print(f'Processing {orixf} to {newxf}')
	convert_xf(orixf, newxf, bin_factor)


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print_usage()
		
	if len(sys.argv) < 4:
		no_proc = 1
	else:
		no_proc = int(sys.argv[3])

	# Use this as a global valuable now
	bin_factor = int(sys.argv[2])
	listfile = sys.argv[1]

	with open(listfile, 'r') as input_list:
		tomo_list = [line.strip() for line in input_list.readlines()]
	
	arg_list = []	
	
	f = open(listfile.replace('.txt', f'_bin{bin_factor}.txt'), 'w')
	
	for tomo in tomo_list:
		arg_list.append((tomo, bin_factor))
		if not os.path.exists(tomo):
			print(f"Error: File '{tomo}' not found.")
			sys.exit(0)

		tspath = os.path.dirname(tomo)
		tsname, tomoxt = os.path.splitext(os.path.basename(tomo))
		f.write(f'{tspath}/{tsname}_bin{bin_factor}.{tomoxt}\n')
		
	f.close()

	print(arg_list)
	
	with multiprocessing.Pool(processes=no_proc) as pool:
		pool.starmap(process_tomo, arg_list)





	