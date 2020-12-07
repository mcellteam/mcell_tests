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


params = m.bngl_utils.load_bngl_parameters('test.bngl')

ITERATIONS = int(params['ITERATIONS'])
    
if 'MCELL_TIME_STEP' in params:
    TIME_STEP = float(params['MCELL_TIME_STEP'])
else:
    TIME_STEP = 1e-6 

if 'MCELL_SUBPARTITION_DIMENSION' in params: 
    MCELL_SUBPARTITION_DIMENSION = float(params['MCELL_SUBPARTITION_DIMENSION'])
else:
    MCELL_SUBPARTITION_DIMENSION = 0.5


# ---- load bngl file ----

model = m.Model()

if 'MCELL_DEFAULT_COMPARTMENT_VOLUME' in params:
    MCELL_DEFAULT_COMPARTMENT_VOLUME = params['MCELL_DEFAULT_COMPARTMENT_VOLUME']
    MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH = MCELL_DEFAULT_COMPARTMENT_VOLUME**(1.0/3.0) 
    default_compartment = m.geometry_utils.create_box(
        'default_compartment', MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH
    )
    model.add_geometry_object(default_compartment)
else:
    MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH = 1
    default_compartment = None
    

model.load_bngl('test.bngl', './react_data/seed_' + str(1).zfill(5) + '/', default_compartment)

for cnt in model.counts:
    cnt.every_n_timesteps = ITERATIONS

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = 1
model.config.total_iterations_hint = ITERATIONS 

model.config.partition_dimension = MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH
model.config.subpartition_dimension = MCELL_SUBPARTITION_DIMENSION 

model.notifications.rxn_and_species_report = False


if os.path.exists('customization.py'):
    import customization
    if 'custom_config' in dir(customization):
        customization.custom_config(model)

model.initialize()

model.run_iterations(ITERATIONS)
model.end_simulation()
