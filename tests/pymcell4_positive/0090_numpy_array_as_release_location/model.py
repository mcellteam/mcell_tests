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

model = m.Model()

a = m.Species('a', diffusion_constant_3d = 0)
model.add_species(a)

rs = m.ReleaseSite(
    'rel_a', a, 
    shape = m.Shape.SPHERICAL,
    location = np.array([0.1, 0.2, 0.3]), 
    number_to_release = 10
)
model.add_release_site(rs)

model.initialize()

model.run_iterations(1)

m0 = model.get_molecule(0)
assert m0.pos3d[0] == 0.1
assert m0.pos3d[1] == 0.2
assert m0.pos3d[2] == 0.3

model.end_simulation()
