#!/usr/bin/env python3

import sys
import os
import math
import numpy as np

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

from parameters import *

if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])


model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- default configuration overrides ----

# ---- add components ----

model.load_bngl('model.bngl')


viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 50
)
model.add_viz_output(viz_output)

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()


# --------------- test ------------------------

# example class passed as context to the callback
class RxnCallbackContext():
    def __init__(self):
        self.count = 0


context_bimol = RxnCallbackContext()
rxn_bimol = model.find_reaction_rule('a_plus_b') 

def rxn_callback_bimol(rxn_info, context):
    assert rxn_info.reaction_rule == rxn_bimol
    context.count += 1

model.register_reaction_callback(
    rxn_callback_bimol, context_bimol, rxn_bimol 
)


context_unimol = RxnCallbackContext()
rxn_unimol = model.find_reaction_rule('d_to_e') 

def rxn_callback_unimol(rxn_info, context):
    assert rxn_info.reaction_rule == rxn_unimol
    context.count += 1

model.register_reaction_callback(
    rxn_callback_unimol, context_unimol, rxn_unimol 
)


model.run_iterations(ITERATIONS)

model.end_simulation()

print("Total number of reactions a_plus_b: " + str(context_bimol.count))
print("Total number of reactions d_to_e: " + str(context_unimol.count))
assert context_bimol.count == 28
assert context_unimol.count == 34

