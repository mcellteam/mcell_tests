#!/usr/bin/env python3

import sys
import os

MCELL_DIR = os.environ.get('MCELL_DIR', '')
if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'lib'))
else:
    print("Error: variable MCELL_DIR that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m


params = m.bngl_utils.load_bngl_parameters('test.bngl')

MCELL_NO_COMPARTMENT_SIZE = params['MCELL_NO_COMPARTMENT_SIZE']
ITERATIONS = int(params['ITERATIONS'])
#VACANCY_SEARCH_DISTANCE = params['VACANCY_SEARCH_DISTANCE'] # not supported by mcell4 yet
SEED = 1
TIME_STEP = 1e-6 # mcell3r converter does not handle this yet  
DUMP = False
EXPORT_DATA_MODEL = True

subsystem = m.Subsystem()
subsystem.load_bngl_molecule_types_and_reaction_rules('test.bngl')

box_no_compartment = m.geometry_utils.create_box(
    'box_no_compartment', MCELL_NO_COMPARTMENT_SIZE
)

instantiation = m.InstantiationData()
instantiation.load_bngl_seed_species('test.bngl', subsystem, box_no_compartment)
instantiation.add_geometry_object(box_no_compartment)


viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    filename_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    all_species = True,
    every_n_timesteps = 1
)

observables = m.Observables()
observables.add_viz_output(viz_output)


model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP # TODO, cannot be in 
model.config.seed = SEED
model.config.total_iterations_hint = ITERATIONS 

model.config.partition_dimension = MCELL_NO_COMPARTMENT_SIZE
model.config.subpartition_dimension = MCELL_NO_COMPARTMENT_SIZE 

model.add_subsystem(subsystem)
model.add_instantiation_data(instantiation)
model.add_observables(observables)

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

model.run_iterations(ITERATIONS)
model.end_simulation()
