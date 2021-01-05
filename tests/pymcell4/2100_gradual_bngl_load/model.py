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

subsystem = m.Subsystem()
subsystem.load_bngl_molecule_types_and_reaction_rules('test.bngl')

box_no_compartment = m.geometry_utils.create_box(
    'box_no_compartment', MCELL_NO_COMPARTMENT_SIZE
)

instantiation = m.Instantiation()
instantiation.load_bngl_seed_species('test.bngl', subsystem, box_no_compartment)
instantiation.add_geometry_object(box_no_compartment)

assert(len(instantiation.release_sites) == 2)

viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)

observables = m.Observables()
observables.load_bngl_observables('test.bngl', subsystem, './react_data/seed_' + str(SEED).zfill(5) + '/')
observables.add_viz_output(viz_output)

assert(len(observables.counts) == 6)

model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP  
model.config.seed = SEED
model.config.total_iterations = ITERATIONS 

model.config.partition_dimension = MCELL_NO_COMPARTMENT_SIZE
model.config.subpartition_dimension = MCELL_NO_COMPARTMENT_SIZE 

model.add_subsystem(subsystem)
model.add_instantiation(instantiation)
model.add_observables(observables)

model.initialize()
model.run_iterations(ITERATIONS)
model.end_simulation()
