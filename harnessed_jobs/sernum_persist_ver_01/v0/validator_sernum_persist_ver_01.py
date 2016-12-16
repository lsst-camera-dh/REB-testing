#!/usr/bin/env python
import os
import lcatr.schema
import eTraveler.clientAPI.connection
import rebUtils

ccs_subsystem = 'ccs-reb5-0'

manufacturerSN = \
    rebUtils.get_serial_number_from_board(ccs_subsystem=ccs_subsystem)
try:
    rebUtils.setManufacturerId(manufacturerId=manufacturerSN)
except Exception as eobj:
    print eobj

rebUtils.check_serial_number(ccs_subsystem=ccs_subsystem)
print "manufacturerSN set to", manufacturerSN

results = [lcatr.schema.valid(lcatr.schema.get('sernum_persist_ver_01'),
                              manufacturerSN=manufacturerSN)]

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
