#!/usr/bin/env python
"""
Producer script for reb_burn_in_ver_03 harnessed job.
"""
from __future__ import print_function
import os
import sys
import socket
import subprocess
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import siteUtils
import rebUtils
import ccs_trending
import file_signal_handler


subsystems = ['ccs-reb5-%i' % i for i in range(3)]
ccs_subsystem = rebUtils.get_ccs_subsystem(subsystems)
results_file = 'burn_in_script_output.txt'
with open(results_file, 'w') as output:
    output.write(ccs_subsystem + '\n')

#
# Loop indefinitely until signal_file is detected.
#
signal_file = os.path.join(os.environ['LCATR_STAGE_ROOT'],
                           'reb_signal_%s.txt' % os.environ['LCATR_JOB_ID'])
signal_handler = file_signal_handler.FileSignalHandler(signal_file)
# 5 hours between reports
report_interval = 5*3600.
while True:
    ntries = 5
    wait_time = 60
    for i in range(ntries):
        try:
#            rebUtils.run_REB5Test_script(ccs_subsystem)
            rebUtils.run_fake_REB5Test_script(ccs_subsystem)
            break
        except subprocess.CalledProcessError as eobj:
            print(str(eobj))
            print("  Try # %i. Waiting %i seconds for next try."
                  % (i, wait_time))
            sys.stdout.flush()
            time.sleep(wait_time)
    signal_handler.wait(report_interval)

# Make trending plots
host = socket.gethostname()
time_axis = ccs_trending.TimeAxis(dt=72)
config_file = os.path.join(os.environ['REBTESTINGDIR'], 'data',
                           'REB_trending_plot.cfg')
config = ccs_trending.ccs_trending_config(config_file)

print("Making trending plots:")
for section in config.sections():
    print("  processing", section)
    plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                           time_axis=time_axis)
    plotter.read_config(config, section)
    plotter.plot()
    plt.savefig('%s_%s_%s.png' % (section, rebUtils.local_time(),
                                  siteUtils.getUnitId()))
