#!/usr/bin/env python3

import sys
import os

ONLY_EXPORT = False

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m


if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])
else:
    SEED = 1
    
bngl_file = os.path.join(MODEL_PATH, 'test.bngl')


params = m.bngl_utils.load_bngl_parameters(bngl_file)


ITERATIONS = int(params['ITERATIONS'])
    
if 'MCELL_TIME_STEP' in params:
    TIME_STEP = float(params['MCELL_TIME_STEP'])
else:
    TIME_STEP = 1e-6 
DUMP = False
EXPORT_DATA_MODEL = False


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
    every_n_timesteps = ITERATIONS
)
model.add_viz_output(viz_output)

gdat_file = ''
if 'GDAT' in params and params['GDAT'] == 1:
    gdat_file = os.path.splitext(os.path.basename(bngl_file))[0] + '.gdat'

model.load_bngl(bngl_file, './react_data/seed_' + str(SEED).zfill(5) + '/' + gdat_file, default_compartment)


# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS 

model.config.partition_dimension = MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH
model.config.subpartition_dimension = MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH 

model.notifications.rxn_and_species_report = True

model.initialize()

# export 
model.export_to_bngl('exported.bngl', m.BNGSimulationMethod.ODE)

if ONLY_EXPORT:
    sys.exit(0)

# and simulate
if DUMP:
    model.dump_internal_state(True)

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

model.run_iterations(ITERATIONS)
model.end_simulation()
