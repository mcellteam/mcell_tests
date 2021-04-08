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
    lib_path = os.path.join(MCELL_PATH, 'lib')
    if os.path.exists(os.path.join(lib_path, 'mcell.so')) or \
        os.path.exists(os.path.join(lib_path, 'mcell.pyd')):
        sys.path.append(lib_path)
    else:
        print("Error: Python module mcell.so or mcell.pyd was not found in "
              "directory '" + lib_path + "' constructed from system variable "
              "MCELL_PATH.")
        sys.exit(1)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)

import mcell as m

# parameters are intentionally not imported using from ... import *
# because we may need to make changes to the module's variables
import parameters

if os.path.exists(os.path.join(MODEL_PATH, 'customization.py')):
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
import observables

import geometry
geometry.up.is_bngl_compartment = True 
geometry.up.surface_compartment_name = 'PM1' 
geometry.bottom.is_bngl_compartment = True 
geometry.bottom.surface_compartment_name = 'PM2'

# create main model object
model = m.Model()

# ---- configuration ----

model.config.time_step = parameters.TIME_STEP
model.config.seed = parameters.SEED
model.config.total_iterations = parameters.ITERATIONS

model.notifications.rxn_and_species_report = True

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.05

# ---- default configuration overrides ----

if customization and 'custom_config' in dir(customization):
    # user-defined model configuration
    customization.custom_config(model)

# ---- add components ----

model.add_subsystem(subsystem.subsystem)
model.add_instantiation(instantiation.instantiation)
model.add_observables(observables.observables)

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
