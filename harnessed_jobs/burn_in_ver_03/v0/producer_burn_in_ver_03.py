#!/usr/bin/env python
from __future__ import print_function
import os
import subprocess
import rebUtils

ccs_subsystem = rebUtils.get_ccs_subsystem()
serial_number = rebUtils.check_serial_number(ccs_subsystem=ccs_subsystem)
print "Manufacturer's serial number set to", serial_number

start_dir = os.path.abspath('.')
command = "burn_in_script"
print(command)
subprocess.check_call(command, shell=True)
os.chdir(start_dir)
