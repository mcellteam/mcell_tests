#!/usr/bin/env python3

# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import sys
import os
import importlib.util

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))


# ---- import mcell module located in directory specified by system variable MCELL_PATH  ----

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    if os.path.exists(os.path.join(lib_path, 'mcell.so')) or \
        os.path.exists(os.path.join(lib_path, 'mcell.pyd')):
        sys.path.append(lib_path)
    else:
        print("Error: Python module mcell.so or mcell.pyd was not found in "
              "directory '" + lib_path + "' constructed from system variable "
              "MCELL_PATH.")
        sys.exit(1)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)

import mcell as m

from geometry import *

# ok
reg1 = box1 * box2
reg2 = reg1 - box2

# wrong
try:
    reg3 = sr1 * box2
    assert False 
except Exception as e:
    print(e)

# wrong as well
try:
    reg3 = sr1 * reg2
    assert False 
except Exception as e:
    print(e)

# ok, although the region is empty in this case
reg4 = sr1 * sr2
