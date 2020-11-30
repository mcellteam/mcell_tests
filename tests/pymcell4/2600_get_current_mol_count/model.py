#!/usr/bin/env python3

import sys
import os
import pandas as pd

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
model.add_instantiation_data(instantiation.instantiation)
model.add_observables(observables.observables)

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()


def load_dat_file(file_name):
    return pd.read_csv(file_name, sep=' ', names=['t', 'v'])

df_a1 = load_dat_file('a.Cube1.dat')
df_a2 = load_dat_file('a.Cube2.dat')
df_a3 = load_dat_file('a.Cube3.dat')
df_aw = load_dat_file('a.World.dat')

count_a_world = model.find_count('a_World')
assert count_a_world

for i in range(ITERATIONS):
    
    model.run_iterations(1)

    # the line index in the reference table is i + 1
    it = i + 1

    c1 = observables.count_a_Cube1.get_current_value()
    assert c1 == df_a1['v'][it]
    
    c2 = observables.count_a_Cube2.get_current_value()
    assert c2 == df_a2['v'][it]
    
    c3 = observables.count_a_Cube3.get_current_value()
    assert c3 == df_a3['v'][it]
    
    cw = count_a_world.get_current_value()
    assert cw == df_aw['v'][it]
    
    
model.end_simulation()
