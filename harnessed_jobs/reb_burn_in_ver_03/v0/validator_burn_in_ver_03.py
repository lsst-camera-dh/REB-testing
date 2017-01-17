#!/usr/bin/env python
"""
Validator script for reb_burn_in_ver_03 harnessed job.
"""
from __future__ import absolute_import, print_function
import lcatr.schema

results_file = 'burn_in_script_output.txt'
with open(results_file) as input_:
    ccs_subsystem = input_.readline().strip()

results = [lcatr.schema.valid(lcatr.schema.get('reb_burn_in_ver_03'),
                              ccs_subsystem=ccs_subsystem)]

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
