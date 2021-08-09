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

ITERATIONS = 10

model = m.Model()


box = m.geometry_utils.create_box(
    'box', 1
)
model.add_geometry_object(box)
    
model.config.total_iterations = ITERATIONS
    
model.initialize()

for i in range(ITERATIONS + 1):
    model.run_iterations(1)
    
    #print(box.__str__(True))
    
    model.add_vertex_move(box, 0, (0.2, 0, 0))
    
    model.apply_vertex_moves(randomize_order=False)

    #print(box.__str__(True))
        

model.end_simulation()


