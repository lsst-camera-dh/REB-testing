#!/usr/bin/env python
"""
Producer script for reb_burn_in_ver_03 harnessed job.
"""
from __future__ import print_function
import os
import shutil
import socket
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import siteUtils
import rebUtils
import ccs_trending

subsystems = ['ccs-reb5-%i' % i for i in range(3)]
ccs_subsystem = rebUtils.get_ccs_subsystem(subsystems)
results_file = 'burn_in_script_output.txt'
with open(results_file, 'w') as output:
    output.write(ccs_subsystem + '\n')

burn_in_script = 'REB5Test.py'
cwd = os.path.abspath('.')

command = "cd /lsst/ccs/REBtest; python %(burn_in_script)s -n -v -C %(ccs_subsystem)s %(cwd)s" % locals()
print(command)

subprocess.check_call(command, shell=True, executable='/bin/bash')

# Create a hard link to the pdf to the cwd for persisting by the
# validator script.
pdf_report = subprocess.check_output('find . -name \*.pdf -print',
                                     shell=True).rstrip()
os.link(pdf_report, os.path.join('.', os.path.basename(pdf_report)))

#fake_report = '/lsst/ccs/tmp/jh_stage/LCA-13574/LCA-13574-010/reb_burn_in_ver_03/v0/5/REB5_Test_17.01.23.22.34_0x189223c1/REB5_Test_17.01.23.22.34_0x189223c1.pdf'
#print("fake the execution of REB5Test.py, copying the report", fake_report)
#shutil.copy(fake_report, 'REB5_Test_fake_report.pdf')

# Make trending plots
host = socket.gethostname()
time_axis = ccs_trending.TimeAxis(dt=72)
config_file = os.path.join(os.environ['REBTESTINGDIR'], 'data',
                           'REB_trending_plot.cfg')
config = ccs_trending.ccs_trending_config(config_file)

print("Making trending plots:")
local_time = ccs_trending.TimeAxis.local_time().isoformat()[:len('2017-01-24T10:44:00')]
for section in config.sections():
    print("  processing", section)
    plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                           time_axis=time_axis)
    plotter.read_config(config, section)
    plotter.plot()
    plt.savefig('%s_%s_%s.png' % (section, local_time, siteUtils.getUnitId()))
