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
SEED = 1
if 'MCELL_TIME_STEP' in params:
    TIME_STEP = float(params['MCELL_TIME_STEP'])
else:
    TIME_STEP = 1e-6 


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
    
viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)
model.add_viz_output(viz_output)

model.load_bngl('test.bngl', './react_data/seed_' + str(SEED).zfill(5) + '/', default_compartment)



# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS 

model.config.partition_dimension = MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH
model.config.subpartition_dimension = MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH 

model.initialize()

model.export_data_model('data_model.json')
