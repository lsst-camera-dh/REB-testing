#!/usr/bin/env python
"""
Validator script for reb5_test_ver_01.
"""
from __future__ import absolute_import, print_function
import glob
import lcatr.schema
import siteUtils
import rebUtils

# Get the most recent pdf reports and text files, in case there are
# multiples because of retries.
pdf_report = sorted(glob.glob('REB5*.pdf'))[-1]
text_file = sorted(glob.glob('REB5*.txt'))[-1]

md = siteUtils.DataCatalogMetadata(LSST_NUM=siteUtils.getUnitId())
results = [lcatr.schema.fileref.make(pdf_report,
                                     metadata=md(DATA_PRODUCT='REB5_REPORT'))]

test_results = rebUtils.parse_REB5Test_results_file(text_file)
schema = lcatr.schema.get('reb5_test_script_results')
for key, value in test_results.items():
    results.append(lcatr.schema.valid(schema, parameter_name=key,
                                      test_result=value))

results.extend(siteUtils.jobInfo())
lcatr.schema.write_file(results)
lcatr.schema.validate_file()
