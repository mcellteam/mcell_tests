#!/usr/bin/env python3

import sys
import os
import numpy as np

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

ITERATIONS = 1

from geometry import *

model = m.Model()

model.add_geometry_object(Tetrahedron)

# ---- initialization and execution ----

v0 = np.array(Tetrahedron_vertex_list[0])
v1 = np.array(Tetrahedron_vertex_list[1])
v2 = np.array(Tetrahedron_vertex_list[2])
n = np.cross(v1-v0, v2-v1)
un_np = n / np.linalg.norm(n)

def assert_eq(a, b):
    assert abs(a - b) < 1e-8

model.initialize()

for i in range(ITERATIONS + 1):
    model.run_iterations(1)
    
    un = model.get_wall_unit_normal(Tetrahedron, 0)
    assert_eq(un.x, un_np[0])
    assert_eq(un.y, un_np[1])
    assert_eq(un.z, un_np[2]) 
    

model.end_simulation()


