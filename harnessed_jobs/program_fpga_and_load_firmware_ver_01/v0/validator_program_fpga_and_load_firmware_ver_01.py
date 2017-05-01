#!/usr/bin/env python
import glob
import lcatr.schema
import siteUtils

vivado_log_files = glob.glob('vivado*.log')
results = [lcatr.schema.fileref.make(log_file) for log_file in vivado_log_files]

results.extend(siteUtils.jobInfo())
lcatr.schema.write_file(results)
lcatr.schema.validate_file()
