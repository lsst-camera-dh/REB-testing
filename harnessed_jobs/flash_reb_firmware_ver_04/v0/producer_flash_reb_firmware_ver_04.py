#!/usr/bin/env python
from __future__ import print_function
import os
import shutil
import subprocess
import rebUtils

logger = rebUtils.get_logger()

reb_afs_path = '/afs/slac/g/lsst/daq/REB_prog_files'
prog_fpga = os.path.join(reb_afs_path, 'prog_fpga.sh')

program_file = os.path.join(reb_afs_path, 'REB_v5_ethernetFW.bit')

command = '%s fpga %s' % (prog_fpga, program_file)
logger.info(command)

output = subprocess.check_output(command, shell=True)
rebUtils.check_REB_vivado_output(output.split('\n'),
                                 expected=('End of startup status: HIGH',))
shutil.copy('vivado.log', 'vivado_fpga.log')
