#!/usr/bin/env python
"""
Validator script for reb_burn_in_ver_03 harnessed job.
"""
from __future__ import absolute_import, print_function
import glob
import lcatr.schema
import siteUtils

results_file = 'burn_in_script_output.txt'
with open(results_file) as input_:
    ccs_subsystem = input_.readline().strip()

results = [lcatr.schema.valid(lcatr.schema.get('reb_burn_in_ver_03'),
                              ccs_subsystem=ccs_subsystem)]

md = siteUtils.DataCatalogMetadata(LSST_NUM=siteUtils.getUnitId(),
                                   producer='SR-REB-VER-03')

pdf_report = glob.glob('REB5*.pdf')[0]
results.append(lcatr.schema.fileref.make(pdf_report,
                                         metadata=md(DATA_PRODUCT='REB5_REPORT')))

for png_file in glob.glob('*.png'):
    dp_name = png_file.split('_')[0] + '_plot'
    results.append(lcatr.schema.fileref.make(png_file,
                                             metadata=md(DATA_PRODUCT=dp_name)))

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
