# NovaCTF Quick Scripts

This repository contains a set of Python scripts designed to simplify the process of running NovaCTF, a software for correcting CTF artifacts in cryo-EM tilt series data.

## Overview
- `novactf_bin_prep.py` Prepare files to run NovaCTF with a binned stack.
- `novactf_paral_auto.py` Run different steps of NovaCTF using a script template for each tomogram individually.
- `novactf_process_list.py` Using novactf_paral_auto.py to run NovaCTF for many tomograms using a tomogram list
- `step 1 to 7 .script files` Template for running novaCTF steps. #n = defocus file number & #ts tilt series name.


## Requirements

- Python 3.3
- NovaCTF ([https://github.com/turonova/novaCTF](https://github.com/turonova/novaCTF))
- Imod ([https://bio3d.colorado.edu/imod/](https://bio3d.colorado.edu/imod/))

## Directory Structure

```
ProjectDir (.)
	├── Tilt series folder (TS_001, TS_002, etc.)
	│   ├── Stack (.st or .mrc)
	│   ├── IMOD files (.xf, .tlt, .xtilt)
	│   └── Defocus file (must be named defocus_file.txt)
	├── Script template (step1 to step7 with appropriate NovaCTF binary and parameters, especially focusing on THICKNESS and IMAGESIZE if you use binned stack)
	└── Tomolist file (contains a list of tomograms to process)
```

## Tomolist File Format

```
TS_001/TS_001_dose-filt.st
TS_002/TS_002_dose-filt.st
...
```

## Running the Scripts

### 1. Binning the Stack

Use `novactf_bin_prep.py` to prepare the files for NovaCTF with a binned stack. This step significantly reduces computational and storage requirements.

```bash
python novaCTF_quick_scripts/novactf_bin_prep.py tomolist bin_factor no_proc
```

Example:

```bash
python novaCTF_quick_scripts/novactf_bin_prep.py tomolist.txt 2 10
```

Output: bin2 stack file, bin2 xf, .tlt, and .txtilt files, and tomolist list file bin 2 (`tomolist_bin2.txt`).

### 2. Running Individual Steps for NovaCTF

Edit the `.script` files in the main project folder with the appropriate parameters. Then, navigate to the tomogram folder (e.g., `TS_001`) and run each step sequentially:
NOTE: Step5 does not deal with xaxistilt right now

- Step 1: Generating defocus file
  ```bash
  python novactf_paral_auto.py ../step1_gendeffile.script TS_001 1
  ```

- Step 2: CTF correction
  ```bash
  python novactf_paral_auto.py ../step2_ctfcorr.script TS_001 10
  ```

- Step 3: Aligning and flipping the stack
  ```bash
  python novactf_paral_auto.py ../step3_align_flip_stack.script TS_001 10
  ```

- Step 4: Filtering projections
  ```bash
  python novactf_paral_auto.py ../step4_filter_proj.script TS_001 10
  ```

- Step 5: Reconstruction (Make sure to check the output to ensure correctness before proceeding with further steps)

  ```bash
  python novactf_paral_auto.py ../step5_recon.script TS_001 1
  ```

- Step 6: Cleaning
  ```bash
  python novactf_paral_auto.py ../step6_clean.script TS_001 1
  ```

- Step 7: Binning (if necessary)
  ```bash
  python novactf_paral_auto.py ../step7_bin.script TS_001 1
  ```

### 3. Running for All Tomograms Simultaneously (Except for Binning Step)

This script will iterate through each tomogram and perform NovaCTF correction using `novactf_paral_auto.py` from steps 1 to 6.

Note: Choose the binned tomolist if you want to perform CTF correction on a binned volume.

```bash
python novactf_process_list.py tomolist no_proc
```

Example:

```bash
python novactf_process_list.py tomolist_bin2.txt 10
```


