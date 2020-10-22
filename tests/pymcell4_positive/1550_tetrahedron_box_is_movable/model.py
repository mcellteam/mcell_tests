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
    location = m.Vec3(0, 0, 0),
    site_diameter = 0,
    number_to_release = 1
)
model.add_release_site(rel)


model.add_geometry_object(Tetrahedron)
    
model.config.total_iterations_hint = ITERATIONS
    
model.initialize()

def assert_eq(a, b):
    #print(a)
    #print(b)
    assert abs(a - b) < 1e-8
    
for i in range(ITERATIONS + 1):
    model.run_iterations(1)
    
    model.export_viz_data_model()
    
    w = model.get_wall(Tetrahedron, 0)
    if i % 3 == 0:
        w.is_movable = not w.is_movable 
            
    for k in range(len(Tetrahedron_vertex_list)):
        model.add_vertex_move(Tetrahedron, k, m.Vec3(0.2, 0.2, 0.2))
    
    #print("XXX " + str(i))
    #print(w.vertices)
    
    if i >= 0 and i <= 3:
        assert_eq(w.vertices[0].x, 0)
    if i == 4:
        assert_eq(w.vertices[0].x, 0.2)
    if i == 5:
        assert_eq(w.vertices[0].x, 0.4)
    if i >= 6 and i <= 9:
        assert_eq(w.vertices[0].x, 0.6)
    if i == 10:
        assert_eq(w.vertices[0].x, 0.8)
        
    model.apply_vertex_moves()

model.end_simulation()


