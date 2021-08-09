#!/usr/bin/env python3

import sys
import os
import random as rnd
import numpy as np

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m


SEED = 1
ITERATIONS = 10
TIME_STEP = 1.00000000e-06
DUMP = True
EXPORT_DATA_MODEL = True


if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])

from geometry import *
from observables import *

model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- add components ----

# TODO viz without any molecules does not work yet
a = m.Species(
    name = 'a',
    diffusion_constant_3d = 1e-6
)
model.add_species(a)
rel = m.ReleaseSite(
    name = 'rel',
    complex = a,
    shape = m.Shape.SPHERICAL,
    location = (8, 8, 8),
    site_diameter = 0,
    number_to_release = 1
)
model.add_release_site(rel)

model.add_geometry_object(Sphere1)
model.add_geometry_object(Sphere2)
model.add_observables(observables)

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model('data_model.json')


    
for i in range(ITERATIONS):
    
    # dump datamodel every N iterations
    if i % 2 == 0:
        model.export_viz_data_model()
            
    for k in range(len(Sphere1_vertex_list)):
        model.add_vertex_move(Sphere1, k, (0.001, 0.001, 0.001))

    model.apply_vertex_moves(randomize_order=False)
            
    model.run_iterations(1)
    

model.end_simulation()
