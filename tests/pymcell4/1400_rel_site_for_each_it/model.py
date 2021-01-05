#!/usr/bin/env python3

import sys
import os
import math

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

SEED = 1
ITERATIONS = 100
TIME_STEP = 1.00000000e-06

model = m.Model()

# add geometry
box = m.geometry_utils.create_box(
    'box', 1
)
model.add_geometry_object(box)

# load our BNGL file and set directory for BNGL observables
model.load_bngl('model.bngl', './react_data/seed_' + str(SEED).zfill(5) + '/')

# set initial count of molecules so that we won't get to copy nr 0 when removing them
# (remove more than exists is ok - in that case all molecules of given species are removed,
# but this would not give us the nice sinusiodal function)
rel = m.ReleaseSite(
    name = 'rel_A_initial',
    complex = m.Complex('A'),
    region = box,
    number_to_release = 1000,
    # and do each release  each iteration
    release_time = 0
)
model.add_release_site(rel)
        
# define release pattern
for i in range(ITERATIONS):
    rel = m.ReleaseSite(
        name = 'rel_A_' + str(i),
        complex = m.Complex('A'),
        region = box,
        # we would like the number of moleucles in the system to follow the sinus curve,
        # derivative of that is cos, number to release is truncated to an integer, may be negative
        number_to_release = 100 * math.cos(i / 10),
        # and do each release  each iteration
        release_time = i * TIME_STEP
    )
    model.add_release_site(rel)
    
# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- initialization and execution ----

model.initialize()

for i in range(ITERATIONS + 1):
    model.run_iterations(1)

model.end_simulation()

