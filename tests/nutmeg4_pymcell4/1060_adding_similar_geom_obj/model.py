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

# single property
box1 = m.geometry_utils.create_box('b1', 1)
box2 = m.geometry_utils.create_box('b1', 1.1)

i1 = m.InstantiationData()
i1.add_geometry_object(box1)
# error
try:
    i1.add_geometry_object(box2)
    assert False
except ValueError as err:
    print(err)


box3 = m.geometry_utils.create_box('b2', 1)
box4 = m.geometry_utils.create_box('b2', 1)

i2 = m.InstantiationData()
i2.add_geometry_object(box3)
# warning
i2.add_geometry_object(box4)
