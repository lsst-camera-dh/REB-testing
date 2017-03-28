#!/usr/bin/env python
"""
Validator script for reb5_continuous_testing_persist.
"""
from __future__ import absolute_import, print_function
import glob
import lcatr.schema
from lcatr.schema import fileref
import siteUtils

results_file = 'ccs_subsystem_info.txt'
with open(results_file) as input_:
    ccs_subsystem = input_.readline().strip()

results = [lcatr.schema.valid(lcatr.schema.get('reb5_continuous_testing'),
                              ccs_subsystem=ccs_subsystem)]

md = siteUtils.DataCatalogMetadata(LSST_NUM=siteUtils.getUnitId())

for pdf_report in glob.glob('REB5*.pdf'):
    results.append(fileref.make(pdf_report,
                                metadata=md(DATA_PRODUCT='REB5_REPORT')))

for png_file in glob.glob('*.png'):
    dp_name = png_file.split('_')[0] + '_plot'
    results.append(fileref.make(png_file,
                                metadata=md(DATA_PRODUCT=dp_name)))

for text_file in glob.glob('*.txt'):
    if text_file == results_file:
        continue
    dp_name = text_file.split('_')[0] + '_plot_data'
    results.append(fileref.make(text_file,
                                metadata=md(DATA_PRODUCT=dp_name)))

results.extend(siteUtils.jobInfo())
lcatr.schema.write_file(results)
lcatr.schema.validate_file()
