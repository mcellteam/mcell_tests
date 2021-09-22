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

v0 = np.array(Tetrahedron_vertex_list[Tetrahedron_wall_list[3][0]])
v1 = np.array(Tetrahedron_vertex_list[Tetrahedron_wall_list[3][1]])
v2 = np.array(Tetrahedron_vertex_list[Tetrahedron_wall_list[3][2]])
v = [v0, v1, v2] 

a = np.linalg.norm(v1-v0)
b = np.linalg.norm(v2-v1)
c = np.linalg.norm(v0-v2)

s = (a + b + c) / 2  
  
# calculate the area  
area = (s*(s-a)*(s-b)*(s-c)) ** 0.5  


# normal
n = np.cross(v1-v0, v2-v1)
un_np = n / np.linalg.norm(n)

def assert_eq(a, b):
    #print(a)
    #print(b)
    assert abs(a - b) < 1e-8
    
model.initialize()

for i in range(ITERATIONS + 1):
    model.run_iterations(1)
    
    w = model.get_wall(Tetrahedron, 3)
    assert w.geometry_object is Tetrahedron
    assert w.wall_index == 3
    
    for i in range(3):
        assert_eq(w.vertices[i][0], v[i][0])
        assert_eq(w.vertices[i][1], v[i][1])
        assert_eq(w.vertices[i][2], v[i][2])
    
    assert_eq(w.area, area)
    assert_eq(np.linalg.norm(w.unit_normal), 1)
    
    un_mn = np.array(w.unit_normal)
    for i in range(3):
        assert_eq(un_mn[i], un_np[i])
        
    assert w.is_movable
    

model.end_simulation()


