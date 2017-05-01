#!/usr/bin/env python
import os
import lcatr.harness.et_wrapper
import lcatr.schema
import siteUtils
import rebUtils

ccs_subsystem = 'REB5tst'

manufacturerSN = \
    rebUtils.get_serial_number_from_board(ccs_subsystem=ccs_subsystem)
try:
    lcatr.harness.et_wrapper.setManufacturerId(manufacturerId=manufacturerSN)
except Exception as eobj:
    print eobj

rebUtils.check_serial_number(ccs_subsystem=ccs_subsystem)
print "manufacturerSN set to", manufacturerSN

results = [lcatr.schema.valid(lcatr.schema.get('sernum_persist_ver_01'),
                              manufacturerSN=manufacturerSN)]

results.extend(siteUtils.jobInfo())
lcatr.schema.write_file(results)
lcatr.schema.validate_file()
