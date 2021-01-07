#!/usr/bin/env python3

# test to check that run_iterations returns correct values 
# and that the simulation is resumed correctly (TODO)

import sys
import os
import time
import threading

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

# ---- import mcell module located in directory ----
# ---- specified by system variable MCELL_PATH  ----
MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    if os.path.exists(os.path.join(lib_path, 'mcell.so')) or \
        os.path.exists(os.path.join(lib_path, 'mcell.dll')):
        sys.path.append(lib_path)
    else:
        print("Error: Python module mcell.so or mcell.dll was not found in "
              "directory '" + lib_path + "' constructed from system variable "
              "MCELL_PATH.")
        sys.exit(1)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)

import mcell as m

import parameters

# create main model object
model = m.Model()

model.load_bngl('model.bngl', './react_data/seed_' + str(parameters.SEED).zfill(5) + '/')

# ---- configuration ----

model.config.time_step = parameters.TIME_STEP
model.config.seed = parameters.SEED
model.config.total_iterations = parameters.ITERATIONS

model.notifications.rxn_and_species_report = False

model.initialize()

if parameters.DUMP:
    model.dump_internal_state()

if parameters.EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()
    
# schedule checkpoint to be run at a given time
def schedule_checkpoint(model_arg):
    print("Checkpoint scheduled")
    model_arg.schedule_checkpoint(0)
        
threading.Timer(2, schedule_checkpoint, [model]).start()

model.run_iterations(parameters.ITERATIONS)

model.end_simulation()
