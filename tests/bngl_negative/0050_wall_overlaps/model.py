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
#VACANCY_SEARCH_DISTANCE = params['VACANCY_SEARCH_DISTANCE'] # not supported by mcell4 yet
SEED = 1
if 'MCELL_TIME_STEP' in params:
    TIME_STEP = float(params['MCELL_TIME_STEP'])
else:
    TIME_STEP = 1e-6 
DUMP = True
EXPORT_DATA_MODEL = True


# ---- load bngl file ----

model = m.Model()

if 'MCELL_NO_COMPARTMENT_SIZE' in params:
    MCELL_NO_COMPARTMENT_SIZE = params['MCELL_NO_COMPARTMENT_SIZE']
    box_no_compartment = m.geometry_utils.create_box(
        'box_no_compartment', MCELL_NO_COMPARTMENT_SIZE
    )
    model.add_geometry_object(box_no_compartment)
else:
    MCELL_NO_COMPARTMENT_SIZE = 1
    box_no_compartment = None
    
viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)
model.add_viz_output(viz_output)

model.load_bngl('test.bngl', './react_data/seed_' + str(SEED).zfill(5) + '/', box_no_compartment)



# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations_hint = ITERATIONS 

model.config.partition_dimension = MCELL_NO_COMPARTMENT_SIZE
model.config.subpartition_dimension = MCELL_NO_COMPARTMENT_SIZE 


model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

model.run_iterations(ITERATIONS)
model.end_simulation()
