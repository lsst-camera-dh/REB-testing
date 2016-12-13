#!/usr/bin/env python
from __future__ import print_function
import os
import subprocess

run_tsreb = os.path.join(os.environ['REBTESTINGDIR'], 'harnessed_jobs',
                         'rebtest_ver_04', 'v0', 'run_tsreb')
reb_id = os.environ["LCATR_UNIT_ID"].split('-')[-1]
command = \
    "/usr/bin/gnome-terminal --command='%(run_tsreb)s %(reb_id)s'" % locals()
print(command)

try:
    subprocess.check_call(command, shell=True, executable='/bin/bash')
except subprocess.CalledProcessError:
    print("Check that REB5 ethernet firmware has been loaded.")
    raise
