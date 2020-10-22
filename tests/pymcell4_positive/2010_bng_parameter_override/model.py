#!/usr/bin/env python3

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

overrides = {'a':4.0, 'c':7.0}

par = m.bngl_utils.load_bngl_parameters('test.bngl', parameter_overrides = overrides)

assert par['a'] == 4.0
assert par['b'] == 4.0 * 5
assert par['c'] == 7.0
