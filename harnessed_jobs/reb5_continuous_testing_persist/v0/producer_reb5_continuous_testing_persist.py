#!/usr/bin/env python
"""
Producer script for persisting data products from REB5 continuous test
jobs that failed but which still have useful data.

This script copies the expected data products to the cwd from the
directory given in the LCATR_REB5_DATA_PRODUCTS_DIR environment
variable.
"""
from __future__ import print_function
import os
import glob
import shutil

def glob_by_file_extension(*file_exts):
    files = []
    for file_ext in file_exts:
        files.extend(os.path.join(os.environ['LCATR_REB5_DATA_PRODUCTS_DIR'],
                                  '*.%s' % file_ext))
    return files

files = glob_by_file_extension('pdf png txt'.split())

for item in files:
    shutil.copy(item '.')
