#!/usr/bin/env python
import lcatr.schema

with open('serial_number.txt') as input_:
    serial_number = input_.readline().strip()

results = [lcatr.schema.valid(lcatr.schema.get('sernum_persist_ver_01'),
                              serial_number=serial_number)]
lcatr.schema.write_file(results)
lcatr.schema.validate_file()

