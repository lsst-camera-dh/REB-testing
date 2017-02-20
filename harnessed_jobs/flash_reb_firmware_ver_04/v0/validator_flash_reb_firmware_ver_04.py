#!/usr/bin/env python
import lcatr.schema
import siteUtils

results = siteUtils.jobInfo()
lcatr.schema.write_file(results)
lcatr.schema.validate_file()
