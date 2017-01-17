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

burn_in_script = os.path.join(os.environ['REBTESTINGDIR'], 'harnessed_jobs',
                              'reb_burn_in_ver_03', 'v0', 'burn_in_script')
outfile = 'burn_in_script_output.txt'
command = "%(burn_in_script)s %(ccs_subsystem)s > %(outfile)s" % locals()
print(command)

subprocess.check_call(command, shell=True, executable='/bin/bash')
