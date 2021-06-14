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

MCELL_NO_COMPARTMENT_SIZE = params['MCELL_NO_COMPARTMENT_SIZE']
assert(float(MCELL_NO_COMPARTMENT_SIZE) == 0.0625)

ITERATIONS = int(params['ITERATIONS'])
assert(ITERATIONS == 10)

SEED = 1
TIME_STEP = 1e-6 # mcell3r converter does not handle this yet  


model = m.Model()

box_no_compartment = m.geometry_utils.create_box(
    'box_no_compartment', MCELL_NO_COMPARTMENT_SIZE
)
model.add_geometry_object(box_no_compartment)

model.load_bngl('test.bngl', './react_data/seed_' + str(SEED).zfill(5) + '/out.gdat', box_no_compartment)

viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)
model.add_viz_output(viz_output)

# ---- configuration ----

model.config.time_step = TIME_STEP  
model.config.seed = SEED
model.config.total_iterations = ITERATIONS 

model.config.partition_dimension = MCELL_NO_COMPARTMENT_SIZE
model.config.subpartition_dimension = MCELL_NO_COMPARTMENT_SIZE 


model.initialize()
model.run_iterations(ITERATIONS)
model.end_simulation()
