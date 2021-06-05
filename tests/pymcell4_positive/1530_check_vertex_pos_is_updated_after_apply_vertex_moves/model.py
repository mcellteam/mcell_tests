#!/usr/bin/env python3

import sys
import os
import copy
import numpy as np

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

from observables import *

ITERATIONS = 2

model = m.Model()


box = m.geometry_utils.create_box(
    'box', 1
)
model.add_geometry_object(box)
    
   
model.add_observables(observables)
    
model.config.total_iterations = ITERATIONS
    
model.initialize()

for i in range(ITERATIONS):
    model.run_iterations(1)
    
    model.add_vertex_move(box, 0, (0.2, 0, 0))
    model.apply_vertex_moves()

    #print(box.__str__(True))
    
    # check that the API side changed
    if i == 0:
        assert box.vertex_list[0][0] == -0.3
    elif i == 1:
        assert box.vertex_list[0][0] == -0.1
    
        

model.end_simulation()


