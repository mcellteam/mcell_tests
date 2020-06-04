#!/usr/bin/env python3

import sys
import os

MCELL_DIR = os.environ.get('MCELL_DIR', '')
if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'lib'))
else:
    print("Error: variable MCELL_DIR that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

model = m.Model()

a = m.Species('a', diffusion_constant_3d = 1e-6)

rs = m.ReleaseSite('rel_a', a, location = m.Vec3(0, 0, 0), number_to_release = 1)
model.add_release_site(rs)
s1 = model.find_release_site('rel_a')
assert s1 != None and s1.name == 'rel_a'
s2 = model.find_release_site('rel_b')
assert s2 == None 
 
g = m.GeometryObject('g', [[0, 0, 0], [1, 1, 1], [0, 0, 1]], [[0, 1, 2]]) 
model.add_geometry_object(g)
g1 = model.find_geometry_object('g')
assert g1 != None and g1.name == 'g'
g2 = model.find_geometry_object('qx')
assert g2 == None 
 