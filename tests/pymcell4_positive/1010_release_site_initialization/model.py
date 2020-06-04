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

model.add_species(a)

rs = m.ReleaseSite('rel_a', a, location = m.Vec3(0, 0, 0), number_to_release = 1)
model.add_release_site(rs)

model.initialize() 