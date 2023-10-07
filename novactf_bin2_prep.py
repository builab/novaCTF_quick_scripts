#!/usr/bin/env python3
# 2023/10 HB, McGill University
# Usage: python novactf_bin2_prep.py tomolist binFactor no_proc


import sys,os,time
from datetime import datetime

def print_usage():
        print("python novactf_bin_prep.py tomolist binFactor no_proc")
        print("e.g.: novactf_bin_prep.py tomolist.txt 2 10");
        sys.exit(0)

if __name__ == "__main__":

        if len(sys.argv) < 3:
                print_usage()

