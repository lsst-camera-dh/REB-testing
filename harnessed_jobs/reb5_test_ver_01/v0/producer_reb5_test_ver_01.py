#!/usr/bin/env python
"""
Producer script for closeout job REB5 test script execution.
"""
from __future__ import print_function
import rebUtils

ccs_subsystem = 'ccs-reb5-ts'

rebUtils.run_REB5Test_script(ccs_subsystem, options='-n -v -e')
