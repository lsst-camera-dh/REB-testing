#!/usr/bin/env python
import subprocess

subprocess.check_call(os.path.join(os.environ['REBTESTINGDIR'], 'bin',
                                   'flash_reb_firmware.sh'), shell=True)

