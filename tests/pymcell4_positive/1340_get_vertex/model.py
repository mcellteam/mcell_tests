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

v2 = np.array(Tetrahedron_vertex_list[2])

def assert_eq(a, b):
    #print(a)
    #print(b)
    assert abs(a - b) < 1e-8
    
model.initialize()

for i in range(ITERATIONS + 1):
    model.run_iterations(1)
    
    vert = model.get_vertex(Tetrahedron, 2)
    assert_eq(v2[0], vert[0])
    assert_eq(v2[1], vert[1])
    assert_eq(v2[2], vert[2])
    

    

model.end_simulation()


