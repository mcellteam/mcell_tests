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
        
        
rxn = model.find_reaction_rule('a_plus_b')


def rxn_callback(rxn_info, context):
    context.count += 1
    
    print(rxn_info.reactant_ids);
    assert len(rxn_info.reactant_ids) == 2
    
    # we are starting with 20 molecules and not creating any new 'a' and 'b'
    assert rxn_info.reactant_ids[0] >= 0 and rxn_info.reactant_ids[0] < 200
    assert rxn_info.reactant_ids[1] >= 0 and rxn_info.reactant_ids[1] < 200
    
    assert rxn_info.reaction_rule is rxn
    
    check_time(rxn_info.time, context.current_it)
    
    check_pos(rxn_info.pos3d)
    
    assert rxn_info.geometry_object is None



context = RxnCallbackContext()
rxn = model.find_reaction_rule('a_plus_b') 

model.register_reaction_callback(
    rxn_callback, context, rxn 
)

for i in range(ITERATIONS + 1):
    context.current_it = i
    model.run_iterations(1)

model.end_simulation()

print("Total number of reactions: " + str(context.count))
assert context.count == 34

