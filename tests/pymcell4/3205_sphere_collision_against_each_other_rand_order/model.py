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
ITERATIONS = 40
TIME_STEP = 1.00000000e-06
DUMP = False
EXPORT_DATA_MODEL = False


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

# TODO viz in cellblender without any molecules does not work yet
a = m.Species(
    name = 'a',
    diffusion_constant_3d = 1e-5
)
model.add_species(a)

b = m.Species(
    name = 'b',
    diffusion_constant_3d = 1e-5
)
model.add_species(b)

rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = a,
    region = Sphere1, 
    number_to_release = 100
)
model.add_release_site(rel_a)

rel_b = m.ReleaseSite(
    name = 'rel_b',
    complex = b,
    region = Sphere2,
    number_to_release = 100
)
model.add_release_site(rel_b)


model.add_geometry_object(Sphere1)
model.add_geometry_object(Sphere2)
model.add_observables(observables)

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()


    
for i in range(ITERATIONS):
    
    # dump datamodel every N iterations
    model.export_viz_data_model()
            
    for k in range(len(Sphere1_vertex_list)):
        model.add_vertex_move(Sphere1, k, (0, 0.01, 0))
        
    for k in range(len(Sphere2_vertex_list)):
        model.add_vertex_move(Sphere2, k, (0, -0.01, 0))

    model.apply_vertex_moves(randomize_order=True)
            
    model.run_iterations(1)
    
    # how to check?
    

model.end_simulation()
