#!/usr/bin/env python
import rebUtils

ccs_subsystem = 'ccs-reb5-0'

serial_number = rebUtils.check_serial_number(ccs_subsystem=ccs_subsystem)
print "Manufacturer's serial number set to", serial_number
