#!/usr/bin/env python3

import sys
import os
import time

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

ITERATIONS = 1000
TIME_STEP = 1e-06


model = m.Model()

a = m.Species(
    name = 'a',
    diffusion_constant_3d = 0
)

rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = a.inst(),
    shape = m.Shape.SPHERICAL,
    location = m.Vec3(0, 0, 0),
    site_diameter = 0,
    number_to_release = 100000
)

# ---- configuration ----

model.config.total_iterations_hint = ITERATIONS 
model.add_species(a)

model.config.memory_limit_gb = 1

model.initialize()

for i in range(ITERATIONS):
    rel_a.release_time = i * TIME_STEP
    model.release_molecules(rel_a)

    model.run_iterations(1)
    
    # do some sleep because the priodicity is 30 seconds and
    # there is no need to use the processor for this test 
    if i > 100:
        time.sleep(2)


model.end_simulation()
