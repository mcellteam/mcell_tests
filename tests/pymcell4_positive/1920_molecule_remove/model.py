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

a = m.Species('a', diffusion_constant_3d = 1e-6)
model.add_species(a)

rs = m.ReleaseSite(
    'rel_a', a, 
    shape = m.Shape.SPHERICAL,
    location = (0, 0, 0), 
    number_to_release = 10
)
model.add_release_site(rs)

model.initialize()

model.run_iterations(1)

all_ids = model.get_molecule_ids()
a_ids = model.get_molecule_ids(a)
assert len(all_ids) == 10
assert all_ids == a_ids

m0 = model.get_molecule(a_ids[1])
assert m0.id == a_ids[1]  # id should be 1

m0.remove()

all_ids2 = model.get_molecule_ids()
assert len(all_ids2) == 9

model.run_iterations(1)

a_ids2 = model.get_molecule_ids(a)
assert len(a_ids2) == 9

model.end_simulation()
