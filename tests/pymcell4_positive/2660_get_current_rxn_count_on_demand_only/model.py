#!/usr/bin/env python3

import sys
import os
#import pandas as pd

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
model.config.total_iterations = ITERATIONS

model.notifications.rxn_and_species_report = True

model.config.partition_dimension = 5
model.config.subpartition_dimension = 2.002

# ---- default configuration overrides ----


# ---- add components ----

model.add_subsystem(subsystem.subsystem)
model.add_instantiation(instantiation.instantiation)
model.add_observables(observables.observables)

# todo: add 


"""
rxn_b_plus_c = model.find_reaction_rule('rxn_b_plus_c')
assert rxn_a_plus_b

count_rxn_b_plus_c = m.Count(
    expression = m.CountTerm(reaction_rule = rxn_b_plus_c)
) 
model.add_count(count_rxn_a_plus_b)
"""

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()


def load_dat_file(file_name):
    res = []
    #return pd.read_csv(file_name, sep=' ', names=['t', 'v'])
    with open(file_name, 'r') as f:
        for line in f:
            count = line.split()[1]
            res.append(int(count))
    
    return res

df_a1 = load_dat_file('rxn_a_plus_b_Cube1.dat')
df_a2 = load_dat_file('rxn_a_plus_b_Cube2.dat')
df_a3 = load_dat_file('rxn_a_plus_b_Cube3.dat')
df_aw = load_dat_file('rxn_a_plus_b_World.dat')

for i in range(ITERATIONS):
    
    model.run_iterations(1)
    

    # the line index in the reference table is i + 1
    it = i + 1

    c1 = observables.count_rxn_a_plus_b_Cube1.get_current_value()
    assert c1 == df_a1[it]
    
    c2 = observables.count_rxn_a_plus_b_Cube2.get_current_value()
    assert c2 == df_a2[it]
    
    c3 = observables.count_rxn_a_plus_b_Cube3.get_current_value()
    assert c3 == df_a3[it]
    
    cw = observables.count_rxn_a_plus_b_World.get_current_value()
    assert cw == df_aw[it]
    
    
model.end_simulation()
