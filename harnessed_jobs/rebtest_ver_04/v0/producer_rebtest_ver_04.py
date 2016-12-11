#!/usr/bin/env python
from __future__ import print_function
import os
import subprocess
import rebUtils

ccs_subsystem = 'ccs-reb5-0'
rebUtils.check_serial_number(ccs_subsystem)

reb_id = os.environ["LCATR_UNIT_ID"].split('-')[-1]

command = "source /opt/lsst/setup_tsreb; /opt/lsst/rebtest/bin/tsreb_wizard --reb-sn %s" % reb_id
print(command)
subprocess.check_call(command, shell=True, executable='/bin/bash')
