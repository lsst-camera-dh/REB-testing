#!/usr/bin/env python
"""
Producer script for closeout job REB5 test script execution.
"""
from __future__ import print_function
import rebUtils

reb_type = rebUtils.get_reb_type()
ccs_subsystem = 'ccs-%s' % reb_type.lower()
rebUtils.run_REB5Test_script(ccs_subsystem, reb_type=reb_type)
