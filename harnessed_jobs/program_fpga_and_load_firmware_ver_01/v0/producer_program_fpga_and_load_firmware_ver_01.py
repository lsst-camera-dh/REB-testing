#!/usr/bin/env python
"""
Producer script for programming the FPGA and uploading the firmware.
"""
from __future__ import print_function
import os
import shutil
import subprocess
import rebUtils

logger = rebUtils.get_logger()

reb_afs_path = '/afs/slac/g/lsst/daq/REB_prog_files'
prog_fpga = os.path.join(reb_afs_path, 'prog_fpga.sh')

# Program the FPGA.
program_file = os.path.join(reb_afs_path, 'REB_v5/reb_v5_daq_v1/reb_v5_2',
                            'REB_v5_top_30325002.bit')
command = '%s fpga %s' % (prog_fpga, program_file)
logger.info(command)

output = subprocess.check_output(command, shell=True)
rebUtils.check_REB_vivado_output(output.split('\n'),
                                 expected=('End of startup status: HIGH',))
shutil.copy('vivado.log', 'vivado_fpga.log')

# Flash the memory.
program_file = os.path.join(reb_afs_path, 'REB_v5/reb_v5_daq_v1/reb_v5_2',
                            'REB_v5_top_30325002.mcs')
command = '%s flash %s' % (prog_fpga, program_file)
logger.info(command)

output = subprocess.check_output(command, shell=True)
rebUtils.check_REB_vivado_output(output.split('\n'))
shutil.copy('vivado.log', 'vivado_flash.log')
