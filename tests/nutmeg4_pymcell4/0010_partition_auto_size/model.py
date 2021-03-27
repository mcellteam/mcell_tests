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

model = m.Model()

box = m.geometry_utils.create_box('box', 10)
model.add_geometry_object(box)

model.config.partition_dimension = 1

model.initialize()

model.run_iterations(1)

model.end_simulation()
