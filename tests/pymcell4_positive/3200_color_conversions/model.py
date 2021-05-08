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

c1 = m.Color(rgba=0xFF0000FF)
c2 = m.Color(1, 0, 0)

assert c1 == c2

c3 = m.Color(rgba=0x003366CC)
c4 = m.Color(0.0, 0.2, 0.4, 0.8) # using values that can be precisely represented
assert c3 == c4

c3.rgba = 0x663366CC
c4.red = 0.4

assert c3 == c4

fail = False
try:
    c5 = m.Color(1.5, 0, 0)
except ValueError:
    fail = True
    
assert fail    
