#!/usr/bin/env python
from __future__ import print_function
import os
import subprocess

reb_id = os.environ["LCATR_UNIT_ID"].split('-')[-1]

command = "source /opt/lsst/setup_tsreb; /opt/lsst/rebtest/bin/tsreb_wizard --reb-sn %s" % reb_id
print(command)

try:
    subprocess.check_call(command, shell=True, executable='/bin/bash')
except subprocess.CalledProcessError:
    print("Check that REB5 ethernet firmware has been loaded.")
    raise
