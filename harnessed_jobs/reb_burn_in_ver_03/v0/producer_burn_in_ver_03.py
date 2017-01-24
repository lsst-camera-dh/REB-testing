#!/usr/bin/env python
"""
Producer script for reb_burn_in_ver_03 harnessed job.
"""
from __future__ import print_function
import os
import subprocess
import rebUtils

subsystems = ['ccs-reb5-%i' % i for i in range(3)]
ccs_subsystem = rebUtils.get_ccs_subsystem(subsystems)
results_file = 'burn_in_script_output.txt'
with open(results_file, 'w') as output:
    output.write(ccs_subsystem + '\n')

burn_in_script = '/lsst/ccs/REBtest/REB5Test.py'
cwd = os.path.abspath('.')

command = "%(burn_in_script)s -n -v -C %(ccs_subsystem)s $(cwd)" % locals()
print(command)

subprocess.check_call(command, shell=True, executable='/bin/bash')
