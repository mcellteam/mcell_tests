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
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])


model = m.Model()


viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = ITERATIONS
)
model.add_viz_output(viz_output)

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations_hint = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- default configuration overrides ----

# ---- add components ----

model.load_bngl('model.bngl')


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
        self.current_it = 0 


def check_time(time, it):
    # cannot start before iteration start
    assert time >= it * TIME_STEP
    # we are running iterations one by one therefore
    # the max time is the end of this iteration 
    assert time <= (it + 1) * TIME_STEP

def check_pos(pos3d):
    EPS = 1e-9
    # min and max coordinates from Cube
    assert pos3d.x >= -0.0625 - EPS and pos3d.x <= 0.0625 + EPS
    assert pos3d.y >= -0.0625 - EPS and pos3d.y <= 0.0625 + EPS
    #print(pos3d.z)
    assert pos3d.z >= -0.0625 - EPS and pos3d.z <= 0.0625 + EPS
        
        
rxn_a_plus_b = model.find_reaction_rule('a_plus_b')
rxn_d_to_e = model.find_reaction_rule('d_to_e')

# this is a bit ugly, we are counting with ds to have ids 200, 201, ... 
next_d_id = 200
rxn_count = 0

def rxn_callback(rxn_info, model):
    global rxn_count
    global next_d_id
    
    rxn_count += 1
    
    # run reaction and change d to e
    model.run_reaction(rxn_d_to_e, [next_d_id], rxn_info.time)
    assert next_d_id < 300
    next_d_id += 1
    
count_c = model.find_count('c')
assert count_c

count_e = model.find_count('e')
assert count_e


model.register_reaction_callback(
    rxn_callback, model, rxn_a_plus_b 
)

model.run_iterations(ITERATIONS)

model.end_simulation()

assert rxn_count == count_c.get_current_value()
assert count_c.get_current_value() == count_e.get_current_value()  

print("Total number of reactions: " + str(rxn_count))
assert rxn_count == 50 # checked against viz output

