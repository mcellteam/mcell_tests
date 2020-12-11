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

from parameters import *

if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value of seed defined in module parameters
    update_seed(int(sys.argv[2]))

import subsystem
import instantiation
import observables

# create main model object
model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = get_seed()
model.config.total_iterations_hint = ITERATIONS

model.notifications.rxn_and_species_report = True

model.config.partition_dimension = 20.02
model.config.subpartition_dimension = 2.002

# ---- default configuration overrides ----


# ---- add components ----

model.add_subsystem(subsystem.subsystem)
model.add_instantiation(instantiation.instantiation)
model.add_observables(observables.observables)

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

def cmp_eq(a, b):
    return abs(a - b) < 1e-9


# retuns none
def find_new_rate(time):
    for t,v in var_rate_react_a_to_b_0:
        if cmp_eq(t, time):
            return v
    return None

rxn = model.find_reaction_rule('a_to_b')
assert rxn

for i in range(ITERATIONS):
    
    r = find_new_rate(i * TIME_STEP)
    if r:
        rxn.fwd_rate = r 
        assert rxn.fwd_rate == r
      
    model.run_iterations(1)
    
model.end_simulation()
