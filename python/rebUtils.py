"""
Utilities for REB-testing harnessed jobs.
"""
from __future__ import print_function
import os
import sys
import datetime
import logging
import subprocess
import socket
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import lcatr.harness.et_wrapper
from PythonBinding import CcsJythonInterpreter
import siteUtils
import ccs_trending

def get_logger(level=logging.INFO):
    logging.basicConfig(format='%(message)s',
                        level=level,
                        stream=sys.stdout)
    return logging.getLogger()

def get_ccs_subsystem(subsystems):
    """
    Poll the specified CCS subsystems to see if the REB under test
    is attached.

    Returns
    -------
    str
        The name of the CCS subsystem with the desired REB attached.
    """
    for item in subsystems:
        try:
            check_serial_number(item)
            return item
        except RebTestingException:
            pass
    message = "No CCS subsystem found for REB %s." % siteUtils.getUnitId()
    raise RebTestingException(message)

class RebTestingException(RuntimeError):
    "REB-testing exception class"
    pass

def check_serial_number(ccs_subsystem, board='REB0'):
    """
    Check the manufacturer's serial number from the REB board via
    CCS versus the manufacturerId in the eTraveler tables.
    """
    sn_board = get_serial_number_from_board(ccs_subsystem, board=board)
    print("ccs subsystem:", ccs_subsystem)
    print("manufacturer's S/N from board:", sn_board)
    sys.stdout.flush()
    sn_eT = lcatr.harness.et_wrapper.getManufacturerId()

    if sn_board != sn_eT:
        message = """The serial number of the installed REB, %s,
does not match the value in the eTraveler
database tables for hardware item %s.""" % (sn_board, siteUtils.getUnitId())
        raise RebTestingException(message)
    return sn_board

def get_serial_number_from_board(ccs_subsystem, board='REB0'):
    """
    Run a CCS script to read the serial number from the board and
    write it to a temporary file as hex.
    """
    temp_file = os.path.join(os.path.abspath('.'), 'serial_number.txt')
    ccs_script = '''from org.lsst.ccs.scripting import *
rafts = CCS.attachSubsystem("%(ccs_subsystem)s")
reb0 = CCS.attachSubsystem("%(ccs_subsystem)s/%(board)s")
result = reb0.synchCommandLine(10, "getSerialNumber")
output = open("%(temp_file)s", 'w')
''' % locals()
    ccs_script += '''output.write('%x\\n' % int(result.getResult()))
output.close()
'''
    ccs = CcsJythonInterpreter(ccs_subsystem)
    result = ccs.sendInterpreterServer(ccs_script)
    result.getOutput()
    with open(temp_file) as input_:
        serial_number = input_.readline().strip()
    os.remove(temp_file)
    return serial_number

def run_REB5Test_script(ccs_subsystem, ntries=5, wait_time=60,
                        script_dir='/lsst/ccs/REBtest',
                        script_name='REB5Test.py',
                        options="-n -v"):
    """
    Run REB5 test script use for REB burn-in and thermal cycling tests.
    """
    # Run fake test for debugging if desired.
    if os.environ.has_key('LCATR_REB5_FAKE_TEST'):
        run_fake_REB5Test_script()
        return
    cwd = os.path.abspath('.')
    command = "cd %(script_dir)s; python %(script_name)s %(options)s -C %(ccs_subsystem)s %(cwd)s" % locals()
    print(command)
    sys.stdout.flush()
    for i in range(ntries):
        print("Attempt #%i to run REB5Test.py" % i)
        try:
            subprocess.check_call(command, shell=True, executable='/bin/bash')
            break
        except subprocess.CalledProcessError as eobj:
            pass
    pdf_report = sorted(subprocess.check_output('find . -name \*.pdf -print',
                                                shell=True).split())[-1]
    text_file = sorted(subprocess.check_output('find . -name REB5\*.txt -print',
                                               shell=True).split())[-1]
    # Create a hard links to the output files to the cwd for persisting
    # by the validator script.
    if os.path.isfile(pdf_report) and os.path.isfile(text_file):
        try:
            os.link(pdf_report, os.path.join('.', os.path.basename(pdf_report)))
            os.link(text_file, os.path.join('.', os.path.basename(text_file)))
        except OSError as eobj:
            print("run_REB5Test_script failed:\n", str(eobj))

def run_fake_REB5Test_script():
    """
    Create a fake REB5 Test report.
    """
    fake_report = 'REB5_Test_fake_report_%s.pdf' % local_time()
    fake_text_file = 'REB5_Test_fake_results_%s.txt' % local_time()
    print("Faking the execution of REB5Test.py, creating the report",
          fake_report)
    sys.stdout.flush()
    for item in (fake_report, fake_text_file):
        with open(item, 'a'):
            os.utime(item, None)

def parse_REB5Test_results_file(results_file):
    """
    Parse the text file produced by the REB5Test.py script and return
    a dictionary of values to be persisted by the validator script to
    the eTraveler results tables
    """
    output = dict()
    with open(results_file) as input_:
        for line in input_:
            tokens = [x.strip() for x in line.split(',')]
            if tokens[0] == 'PASS':
                ikey = 1
                ivalue = 0
            else:
                ikey = 0
                ivalue = 1
            output[tokens[ikey].replace(' ', '_')] = tokens[ivalue]
    return output

def local_time():
    """
    Return the current local time in ISO-8601 format.
    """
    return datetime.datetime.now().isoformat()[:len('2017-01-24T10:44:00')]

def make_ccs_trending_plots(ccs_subsystem, dt=None, start=None, end=None,
                            nbins=None, config_file=None):
    """
    Make trending plots.

    Parameters
    ----------
    ccs_subsystem : str
        CCS subsystem name, e.g., 'ccs-reb5-0'.
    dt : float, optional
        Duration of time axis in hours.  Ignored if both start and
        end are given.  Default: 24.
    start : str, optional
        Start of time interval. ISO-8601 format, e.g., "2017-01-21T09:58:01"
    end : str, optional
        End of time interval. ISO-8601 format.
    nbins : int, optional
        Number of bins for time axis.  Automatically chosen by RESTful
        server if not given.
    config_file : str, optional
        Configuration file listing the trending quantities to plot.
        If None (default), then use the config file in
        REB-testing/data/REB_trending_plot.cfg.

    Notes
    -----
    This function writes the trending plots as png files in the cwd.
    The filenames are of the form
    <trending quantity>_<local time>_<LSST SN>.png.
    """
    host = socket.gethostname()
    time_axis = ccs_trending.TimeAxis(dt=dt, start=start, end=end, nbins=nbins)
    if config_file is None:
        config_file = os.path.join(os.environ['REBTESTINGDIR'], 'data',
                                   'REB_trending_plot.cfg')
    config = ccs_trending.ccs_trending_config(config_file)

    print("Making trending plots:")
    for section in config.sections():
        print("  processing", section)
        sys.stdout.flush()
        try:
            plotter = ccs_trending.TrendingPlotter(ccs_subsystem, host,
                                                   time_axis=time_axis)
            plotter.read_config(config, section)
            plotter.plot()
            plt.savefig('%s_%s_%s.png' % (section, local_time(),
                                          siteUtils.getUnitId()))
            plotter.save_file('%s_%s_%s.txt' % (section, local_time(),
                                                siteUtils.getUnitId()))
        except StandardError as eobj:
            print("Exception caught while trying to generate plot:")
            print(str(eobj))
            print("Skipping %s plot." % section)

class RebProgrammingError(RuntimeError):
    def __init__(self, *args, **kwds):
        super(RebProgrammingError, self).__init__(*args, **kwds)

def check_REB_vivado_output(lines,
                            expected=('Erase Operation successful.',
                                      'Program/Verify Operation successful.',
                                      'Flash programming completed successfully',
                                      'Done pin status: HIGH')):
    expected_text = set(expected)
    for line in lines:
        for item in expected:
            if item in line:
                expected_text.remove(item)
    if expected_text:
        raise RebProgrammingError("Failure flashing REB memory. "
                                  + "Missing expected lines from vivado.log:\n"
                                  + '\n'.join(expected_text))
