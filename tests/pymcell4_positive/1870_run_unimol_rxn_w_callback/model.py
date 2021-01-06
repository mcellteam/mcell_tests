#!/usr/bin/env python3

# test to check GIL lock/unlock works correctly when run_reaction is called

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

rxn_a_to_c = model.find_reaction_rule('a_to_c')

callbacks_called = 0

def rxn_callback(rxn_info, model):
    global callbacks_called
    callbacks_called += 1
    if rxn_info.reactant_ids[0] == 0:
        # run one more reaction
        products = model.run_reaction(rxn_a_to_c, [1], 1.8)
        assert len(products) == 1 and products[0] == 101

        
model.register_reaction_callback(
    rxn_callback, model, rxn_a_to_c 
)
   
model.run_iterations(1)

# there are only As, so index 0 is safe
products = model.run_reaction(rxn_a_to_c, [0], 1.5)
assert len(products) == 1 and products[0] == 100

assert callbacks_called == 2

model.end_simulation()
