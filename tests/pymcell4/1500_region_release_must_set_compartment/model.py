#!/usr/bin/env python3

# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import sys
import os

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

# ---- import mcell module located in directory ----
# ---- specified by system variable MCELL_PATH  ----
MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

# parameters are intentionally not imported using from ... import *
# because we may need to make changes to the module's variables
import parameters

if os.path.exists(os.path.join('customization.py')):
    import customization
else:
    customization = None

if customization and 'custom_argparse_and_parameters' in dir(customization):
    # custom argument processing and parameter setup
    customization.custom_argparse_and_parameters()
else:
    if len(sys.argv) == 1:
        # no arguments
        pass
    elif len(sys.argv) == 3 and sys.argv[1] == '-seed':
        # overwrite value of seed defined in module parameters
        parameters.SEED = int(sys.argv[2])
    else:
        print("Error: invalid command line arguments")
        print("  usage: " + sys.argv[0] + "[-seed N]")
        sys.exit(1)

import subsystem
import instantiation

# create main model object
model = m.Model()

# ---- configuration ----

model.config.time_step = parameters.TIME_STEP
model.config.seed = parameters.SEED
model.config.total_iterations = parameters.ITERATIONS

model.notifications.rxn_and_species_report = True

model.config.partition_dimension = 0.75
model.config.subpartition_dimension = 0.125

# ---- default configuration overrides ----

if customization and 'custom_config' in dir(customization):
    # user-defined model configuration
    customization.custom_config(model)

# ---- add components ----

viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(parameters.SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)
model.add_viz_output(viz_output)

count_Syk_CP = m.Count(
    molecules_pattern = m.Complex('Syk@CP'),
    file_name = './react_data/seed_' + str(parameters.SEED).zfill(5) + '/Syk.dat',
    every_n_timesteps = 1
)
model.add_count(count_Syk_CP)

model.add_subsystem(subsystem.subsystem)
model.add_instantiation(instantiation.instantiation)

# ---- initialization and execution ----

if customization and 'custom_init_and_run' in dir(customization):
    customization.custom_init_and_run(model)
else:
    model.initialize()

    if parameters.DUMP:
        model.dump_internal_state()

    if parameters.EXPORT_DATA_MODEL and model.viz_outputs:
        model.export_data_model()

    model.run_iterations(parameters.ITERATIONS)
    model.end_simulation()
