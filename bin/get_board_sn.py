#!/usr/bin/env python
"""
Application to get a REB board's manufacturer's serial number in hex.
"""
from __future__ import print_function
import argparse
import rebUtils

parser = argparse.ArgumentParser(description="Get REB board S/N for the requested CCS subsystem")
parser.add_argument('ccs_subsystem', type=str,
                    help='CCS subsystem, e.g., ccs-reb5-0')
args = parser.parse_args()

print("Manufacturer's serial number:",
      rebUtils.get_serial_number_from_board(args.ccs_subsystem))
