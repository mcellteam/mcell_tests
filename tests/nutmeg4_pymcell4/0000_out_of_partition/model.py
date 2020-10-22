#!/usr/bin/env python3

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

model = m.Model()

a = m.Species('a', diffusion_constant_3d = 1e-4)
model.add_species(a)

rs = m.ReleaseSite(
    'rel_a', a, 
    shape = m.Shape.SPHERICAL,
    location = m.Vec3(0, 0, 0), 
    number_to_release = 10
)
model.add_release_site(rs)

model.initialize()

model.run_iterations(1000)

model.end_simulation()
