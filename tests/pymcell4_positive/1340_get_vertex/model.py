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

def assert_raises(error_type, text, function, *args):
    try:
        function(*args)
    except error_type as e:
        assert str(e) == text, 'unexpected text: ' + str(e)
        return
    assert False, 'expected ' + error_type.__name__ + ': ' + text

# get_vertex checks its arguments as the other geometry getters do; before
# initialization, and with None, it used to end Python with a segmentation fault
assert_raises(
    RuntimeError, 'Geometry object Tetrahedron is not present in model (or model was not initialized).',
    model.get_vertex, Tetrahedron, 2)

model.initialize()

assert_raises(ValueError, 'Argument passed as GeometryObject must not be None.', model.get_vertex, None, 2)

for i in range(ITERATIONS + 1):
    model.run_iterations(1)
    
    vert = model.get_vertex(Tetrahedron, 2)
    assert_eq(v2[0], vert[0])
    assert_eq(v2[1], vert[1])
    assert_eq(v2[2], vert[2])
    

    

model.end_simulation()


