#!/usr/bin/env python
"""
Producer script for scheduled [GW]REB continuous test script executions.
"""
from __future__ import print_function
import os
import sys
import time
import rebUtils
import file_signal_handler

reb_type = rebUtils.get_reb_type()

# Write the ccs_subsystem to the text file.
ccs_subsystem = 'ccs-%s' % reb_type.lower()
results_file = 'ccs_subsystem_info.txt'
with open(results_file, 'w') as output:
    output.write(ccs_subsystem + '\n')

tstart = time.time()

# Loop indefinitely until the signal file is detected.
signal_handler = file_signal_handler.FileSignalHandler()

# Use 6 hours between reports, unless overridden.
report_interval = float(os.environ.get('LCATR_REB5_TEST_INTERVAL', 6.*60.*60.))
print("Generating %s test reports every %.2f hours"
      % (reb_type, report_interval/3600.))
sys.stdout.flush()
try:
    while True:
        rebUtils.run_REB5Test_script(ccs_subsystem, reb_type=reb_type)
        signal_handler.wait(report_interval)
except file_signal_handler.FileSignalHandlerException:
    pass

elapsed_hours = (time.time() - tstart)/3600.
config_file = os.path.join(os.environ['REBTESTINGDIR'], 'data',
                           '%s_trending_plot.cfg' % reb_type)
rebUtils.make_ccs_trending_plots(ccs_subsystem, dt=elapsed_hours,
                                 config_file=config_file)
