#!/usr/bin/env python
"""
Validator script for reb5_closeout_test.
"""
from __future__ import absolute_import, print_function
import glob
import lcatr.schema
import siteUtils

# Get the last one, if there are multiples because of retries.
pdf_report = sorted(glob.glob('REB5*.pdf'))[-1]

md = siteUtils.DataCatalogMetadata(LSST_NUM=siteUtils.getUnitId())
results = [lcatr.schema.fileref.make(pdf_report,
                                     metadata=md(DATA_PRODUCT='REB5_REPORT'))]

lcatr.schema.write_file(results)
lcatr.schema.validate_file()
