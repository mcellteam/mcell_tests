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

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.05

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

def get_mol_pos_bins():
    res = {}
    
    # get list of all molecule ids
    id_list = model.get_molecule_ids()
    for id in id_list:
        # and create a histogram based on their y position
        m = model.get_molecule(id)
        
        # 5 bins, y is in range -0.25..0.25
        y = m.pos3d.y
        bin = int((y + 0.25) * 1/0.5*5)
        
        if bin in res:
            res[bin] += 1
        else:
            res[bin] = 0
    return res

for i in range(10):
    # first run 1000 iterations
    model.run_iterations(1000)
    
    counts_per_y_bin = get_mol_pos_bins()
    sorted_bins = sorted(counts_per_y_bin.items())
    for k,v in sorted_bins:
        print(str(k) + ":" + str(v))
    print("---------")
    
    for k in range(len(sorted_bins) - 1):
        # check that the number of molecules decreases from left to right
        # for higher number of bins/different seed this might not be true all the time
        assert(sorted_bins[k][1] > sorted_bins[k + 1][1])

model.end_simulation()
