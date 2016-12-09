"""
Utilities for REB-testing harnessed jobs.
"""
import lcatr.harness.et_wrapper
import siteUtils
from PythonBinding import CcsJythonInterpreter

class RebTestingException(RuntimeError):
    "REB-testing exception class"
    pass

def check_manufacturer_SN(ccs_system_name='ccs-reb4', verbose=True):
    """
    Check the manufacturer's SN from the board (via CCS) versus
    the manufacturer's SN (ID) in the eTraveler tables.
    """
    sn_board = get_manufacturer_SN_from_board(ccs_system_name, verbose)
    sn_eT = lcatr.harness.et_wrapper.getManufacturerId()

    if sn_board != sn_eT:
        message = """The serial number of the installed REB, %s,
does not match the value in the eTraveler
database tables for hardware item %s.""" % (sn_board, siteUtils.getUnitId())
        raise RebTestingException(message)

def get_manufacturer_SN_from_board(ccs_system_name='ccs-reb4', verbose=True):
    """
    Run the serialNumber.py CCS script to read the serial number from
    the board.
    """
    ccs = CcsJythonInterpreter(ccs_system_name)
    ccs_script = os.path.join(os.environ['REB_TESTINGDIR'], 'python',
                              'serialNumber.py')
    result = ccs.syncScriptExecution(ccs_script, verbose=verbose)
    with open('serial_number.txt') as input_:
        manufacturer_SN = input_.readline().strip()
    return manufacturer_SN
