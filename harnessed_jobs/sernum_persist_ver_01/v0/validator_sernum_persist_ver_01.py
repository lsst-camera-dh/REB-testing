#!/usr/bin/env python
import os
import lcatr.schema
import lcatr.harness.et_wrapper
import rebUtils

ccs_subsystem = 'ccs-reb4'

manufacturerSN = get_serial_number_from_board(ccs_subsystem=ccs_subsystem)
try:
    lcatr.harness.et_wrapper.setManufacturerId(manufacturerId=manufacturerSN)
except Exception as eobj:
    print eobj

rebUtils.check_serial_number(ccs_subsystem=ccs_subsystem)
print "manufacturerSN set to", manufacturerSN

results = [lcatr.schema.valid(lcatr.schema.get('sernum_persist_ver_01'),
                              manufacturerSN=manufacturerSN)]

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
