#!/usr/bin/env python
"""
Validator script for reb5_closeout_test.
"""
from __future__ import absolute_import, print_function
import glob
import lcatr.schema
import siteUtils
import rebUtils

reb_type = rebUtils.get_reb_type()
# Get the most recent pdf reports and text files, in case there are
# multiples because of retries.
pdf_report = sorted(glob.glob('%s*.pdf' % reb_type))[-1]
text_file = sorted(glob.glob('%s*.txt' % reb_type))[-1]

md = siteUtils.DataCatalogMetadata(LSST_NUM=siteUtils.getUnitId())
results = [lcatr.schema.fileref.make(pdf_report,
                                     metadata=md(DATA_PRODUCT='%s_REPORT' % reb_type))]

test_results = rebUtils.parse_REB5Test_results_file(text_file)
schema = lcatr.schema.get('reb5_test_script_results')
for key, value in test_results.items():
    results.append(lcatr.schema.valid(schema, parameter_name=key,
                                      test_result=value))

results.extend(siteUtils.jobInfo())
lcatr.schema.write_file(results)
lcatr.schema.validate_file()
