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

def glob_by_file_extension(file_exts):
    files = []
    dp_dir = os.environ['LCATR_REB5_DATA_PRODUCTS_DIR']
    for file_ext in file_exts:
        glob_string = os.path.join(dp_dir, '*.%s' % file_ext)
        files.extend(glob.glob(glob_string))
    return files

files = glob_by_file_extension('pdf png txt'.split())

print("copying")
for item in files:
    print(item)
    shutil.copy(item, os.path.abspath('.'))
