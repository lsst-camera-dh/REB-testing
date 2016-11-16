#!/usr/bin/env python
import os
import lcatr.schema
#import eTraveler.clientAPI.connection
import lcatr.harness.et_wrapper

#operator = os.environ['LCATR_OPERATOR']
#db = os.path.split(os.environ['LCATR_LIMS_URL'])[-1]
#if db not in 'Prod Dev'.split():
#    db = 'Dev'
#conn = eTraveler.clientAPI.connection.Connection(operator=operator, db=db)

with open('serial_number.txt') as input_:
    manufacturerSN = input_.readline().strip()

#experimentSN = os.environ['LCATR_UNIT_ID']
#htype = os.environ['LCATR_UNIT_TYPE']
try:
    lcatr.harness.et_wrapper.setManufacturerId(manufacturerId=manufacturerSN)
    #conn.setManufacturerId(experimentSN=experimentSN, htype=htype,
    #                       manufacturerId=manufacturerSN)
except Exception as eobj:
    print eobj

print "manufacturerSN set to", \
    #conn.getManufacturerId(experimentSN=experimentSN, htype=htype)
    lcatr.harness.et_wrapper.getManufacturerId()

results = [lcatr.schema.valid(lcatr.schema.get('sernum_persist_ver_01'),
                              manufacturerSN=manufacturerSN)]

lcatr.schema.write_file(results)
lcatr.schema.validate_file()

