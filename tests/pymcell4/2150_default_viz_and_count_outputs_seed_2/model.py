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


params = m.bngl_utils.load_bngl_parameters('test1.bngl')

MCELL_NO_COMPARTMENT_SIZE = params['MCELL_NO_COMPARTMENT_SIZE']
assert(float(MCELL_NO_COMPARTMENT_SIZE) == 0.0625)

ITERATIONS = int(params['ITERATIONS'])
assert(ITERATIONS == 10)

SEED = 2
TIME_STEP = 1e-6 # mcell3r converter does not handle this yet  

box_no_compartment = m.geometry_utils.create_box(
    'box_no_compartment', MCELL_NO_COMPARTMENT_SIZE
)


viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    #output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)

count = m.Count(
    name = 'Cmol',
    #file_name = './react_data/seed_' + str(SEED).zfill(5) + '/' + 'Cmol' + '.dat',
    expression = m.CountTerm(
        molecules_pattern = m.Complex('C')
    ) 
)

observables = m.Observables()
observables.load_bngl_observables('test2.bngl') #, './react_data/seed_' + str(SEED).zfill(5) + '/')
observables.add_viz_output(viz_output)
observables.add_count(count)


model = m.Model()

model.add_geometry_object(box_no_compartment)
model.load_bngl(
    'test1.bngl', 
    #'./react_data/seed_' + str(SEED).zfill(5) + '/', 
    default_release_region = box_no_compartment)

# ---- configuration ----

model.config.time_step = TIME_STEP  
model.config.seed = SEED
model.config.total_iterations = ITERATIONS 

model.config.partition_dimension = MCELL_NO_COMPARTMENT_SIZE
model.config.subpartition_dimension = MCELL_NO_COMPARTMENT_SIZE 

model.add_observables(observables)

model.initialize()
model.run_iterations(ITERATIONS)
model.end_simulation()
