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

from geometry import *
from observables import *

model = m.Model()

model.add_observables(observables)

# TODO viz in cellblender without any molecules does not work yet
a = m.Species(
    name = 'a',
    diffusion_constant_3d = 0
)
model.add_species(a)
rel = m.ReleaseSite(
    name = 'rel',
    complex = a,
    shape = m.Shape.SPHERICAL,
    location = (0, 0, 0),
    site_diameter = 0,
    number_to_release = 1
)
model.add_release_site(rel)


Tetrahedron.translate((-0.2, 0, 0))

model.add_geometry_object(Tetrahedron)

box_no_compartment = m.geometry_utils.create_box(
    'box_no_compartment', 0.2
)
model.add_geometry_object(box_no_compartment)
    
model.config.total_iterations = ITERATIONS
    
model.initialize()

for i in range(ITERATIONS + 1):
    model.export_viz_data_model()
            
    for k in range(len(Tetrahedron_vertex_list) - 1): # not moving with the last vertex
        model.add_vertex_move(Tetrahedron, k, (0.02, 0, 0))
        
    model.apply_vertex_moves()
    
    model.run_iterations(1)
    
    # vertex must not move into the box 
    v1 = model.get_vertex(Tetrahedron, 0)
    assert v1.x < -0.1
    
    v2 = model.get_vertex(Tetrahedron, 1)
    # vertex must not move into 
    assert v2.x < -0.1

    v3 = model.get_vertex(Tetrahedron, 2)
    # vertex must not move into 
    assert v3.x < -0.1
    

model.end_simulation()


