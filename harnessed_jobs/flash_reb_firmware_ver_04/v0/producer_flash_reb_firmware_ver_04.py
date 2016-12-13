#!/usr/bin/env python
from __future__ import print_function
import os
import subprocess

start_dir = os.path.abspath('.')
os.chdir('/afs/slac/g/lsst/daq/REB_prog_files')
command = './prog_fpga.sh fpga ./../../../../../../data/REB_v5_ethernet-20161202.bit'
print(command)
subprocess.check_call(command, shell=True)
os.chdir(start_dir)
