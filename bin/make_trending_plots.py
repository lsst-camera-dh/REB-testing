#!/usr/bin/env python
"""
Application to make CCS trending plots given a config file.
"""
import os
import argparse
import rebUtils

parser = argparse.ArgumentParser(description="Make CCS trending plots.")
parser.add_argument("config_file", type=str,
                    help="Config file with lists of quantities to plot.")
parser.add_argument("ccs_subsystem", type=str,
                    help="CCS subsystem, e.g., 'ccs-reb5-0'.")
parser.add_argument("--dt", type=float, default=24,
                    help="Plotting interval duration (hours).  Default: 24")
parser.add_argument("--end_datetime", type=str, default=None,
                    help="Ending datetime of plotting interval (ISOT).  Default: now")
parser.add_argument("--nbins", type=int, default=100,
                    help="Number of time bins.  Default: 100")
args = parser.parse_args()

if not os.environ.has_key('LCATR_UNIT_ID'):
    os.environ['LCATR_UNIT_ID'] = 'UNSET_LCATR_UNIT_ID'

rebUtils.make_ccs_trending_plots(args.ccs_subsystem,
                                 dt=args.dt,
                                 end=args.end_datetime,
                                 nbins=args.nbins,
                                 config_file=args.config_file)
