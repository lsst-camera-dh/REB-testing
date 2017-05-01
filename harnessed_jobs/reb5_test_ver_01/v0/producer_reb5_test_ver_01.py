#!/usr/bin/env python
"""
Producer script for closeout job REB5 test script execution.
"""
from __future__ import print_function
import rebUtils

subsystems = ['ccs-reb5-%i' % i for i in range(3)]
ccs_subsystem = rebUtils.get_ccs_subsystem(subsystems)

rebUtils.run_REB5Test_script(ccs_subsystem, options='-n -v -e')
