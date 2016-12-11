#!/usr/bin/env python
from __future__ import print_function
import os
import subprocess

reb_id = os.environ["LCATR_UNIT_ID"].split('-')[1]

command = "source /opt/lsst/setup_tsreb; tsreb_wizard --reb-sn %s" % reb_id
print(command)
subprocess.check_call(command, shell=True, executable='/bin/bash')
