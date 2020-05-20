#!/usr/bin/env python3

# based on mcell_tests/tests/mdl/0320_2_mols_react_in_box_it_10
# rewritten to look like a generated file 

import sys
import os

MCELL_DIR = os.environ.get('MCELL_DIR', '')
if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'lib'))
else:
    print("Error: variable MCELL_DIR that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

from parameters import *
import subsystem
import instantiation
import observables


model = m.Model()

# --- configuration ---

model.config.time_step = TIME_STEP # default
model.config.seed = SEED
model.config.total_iterations_hint = ITERATIONS

model.config.partition_dimension = 20
model.config.subpartition_dimension = 2


# -- add components ---

model.add_subsystem(subsystem.subsystem)
model.add_instantiation_data(instantiation.instantiation)
model.add_observables(observables.observables)


# --- initialization and execution ---

model.initialize()

if DUMP:
    model.dump_internal_state()

model.run_iterations(ITERATIONS)
model.end_simulation()
