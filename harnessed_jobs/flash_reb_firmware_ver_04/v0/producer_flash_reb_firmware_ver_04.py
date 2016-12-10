#!/usr/bin/env python
import subprocess
import rebUtils

ccs_subsystem = 'ccs-reb5-0'

rebUtils.check_serial_number(ccs_subsystem)

subprocess.check_call(os.path.join(os.environ['REBTESTINGDIR'], 'bin',
                                   'flash_reb_firmware.sh'), shell=True)

