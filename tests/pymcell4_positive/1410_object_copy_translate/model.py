#!/usr/bin/env python3

import sys
import os
import copy
import numpy as np

MCELL_DIR = os.environ.get('MCELL_DIR', '')
if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'lib'))
else:
    print("Error: variable MCELL_DIR that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

ITERATIONS = 1

from geometry import *

model = m.Model()

Tetrahedron1 = Tetrahedron
Tetrahedron2 = copy.deepcopy(Tetrahedron) 

Tetrahedron2.translate(m.Vec3(0.1, 0.1, 0.1))

model.add_geometry_object(Tetrahedron1)
model.add_geometry_object(Tetrahedron2)

# ---- initialization and execution ----

v0 = np.array(Tetrahedron_vertex_list[Tetrahedron_element_connections[0][0]])
v1 = np.array(Tetrahedron_vertex_list[Tetrahedron_element_connections[0][1]])
v2 = np.array(Tetrahedron_vertex_list[Tetrahedron_element_connections[0][2]])
v = [v0, v1, v2] 

def assert_eq(a, b):
    print(a)
    print(b)
    assert abs(a - b) < 1e-8

    
model.initialize()

for i in range(ITERATIONS + 1):
    model.run_iterations(1)
    
    w1 = model.get_wall(Tetrahedron2, 0)
    
    for i in range(3):
        assert_eq(v[i][0] + 0.1, w1.vertices[i].x)
        assert_eq(v[i][1] + 0.1, w1.vertices[i].y)
        assert_eq(v[i][2] + 0.1, w1.vertices[i].z)
    

    

model.end_simulation()


