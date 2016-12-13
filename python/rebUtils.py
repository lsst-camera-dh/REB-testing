"""
Utilities for REB-testing harnessed jobs.
"""
import os
#import lcatr.harness.et_wrapper
import eTraveler.clientAPI.connection
from PythonBinding import CcsJythonInterpreter
import siteUtils

def get_ccs_subsystem():
    raise NotImplemented("This function is not implemented.")

def get_eT_connection():
    operator = os.environ['LCATR_OPERATOR']
    db = os.path.split(os.environ['LCATR_LIMS_URL'])[-1]
    if db not in 'Prod Dev'.split():
        # This case occurs when using the fake_eT server, so set db to 'Dev'.
        db = 'Dev'
    return eTraveler.clientAPI.connection.Connection(operator=operator, db=db)

def setManufacturerId(manufacturerId):
    conn = get_eT_connection()
    experimentSN = os.environ['LCATR_UNIT_ID']
    htype = os.environ['LCATR_UNIT_TYPE']
    conn.setManufacturerId(experimentSN=experimentSN, htype=htype,
                           manufacturerId=manufacturerId)

def getManufacturerId():
    conn = get_eT_connection()
    experimentSN = os.environ['LCATR_UNIT_ID']
    htype = os.environ['LCATR_UNIT_TYPE']
    return conn.getManufacturerId(experimentSN=experimentSN, htype=htype)

class RebTestingException(RuntimeError):
    "REB-testing exception class"
    pass

def check_serial_number(ccs_subsystem, board='REB0'):
    """
    Check the manufacturer's serial number from the REB board via
    CCS versus the manufacturerId in the eTraveler tables.
    """
    sn_board = get_serial_number_from_board(ccs_subsystem, board=board)
#    sn_eT = lcatr.harness.et_wrapper.getManufacturerId()
    sn_eT = getManufacturerId()

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
