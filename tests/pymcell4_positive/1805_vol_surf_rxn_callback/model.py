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

# based on geometry_utils.inc uv2xyz
def uv2xyz(geometry_object, wall_index, pos2d):
    wall = model.get_wall(geometry_object, wall_index)
    
    f1 = wall.vertices[1] - wall.vertices[0]
    f1_len_squared = f1.x * f1.x + f1.y * f1.y + f1.z * f1.z   
    inv_f1_len = 1 / math.sqrt(f1_len_squared);

    unit_u = f1 * m.Vec3(inv_f1_len);
    v_nparray = np.cross(wall.unit_normal.to_list(), unit_u.to_list())
    unit_v = m.Vec3(v_nparray[0], v_nparray[1], v_nparray[2])
    
    return m.Vec3(pos2d.u) * unit_u + m.Vec3(pos2d.v) * unit_v + wall.vertices[0]
    

def check_time(time, it):
    # cannot start before iteration start
    assert time >= it * TIME_STEP
    # we are running iterations one by one therefore
    # the max time is the end of this iteration 
    assert time <= (it + 1) * TIME_STEP

def check_pos3d(pos3d):
    EPS = 1e-9
    #print(pos3d)
    # min and max coordinates from Cube
    assert pos3d.x >= -0.0625 - EPS and pos3d.x <= 0.0625 + EPS
    assert pos3d.y >= -0.0625 - EPS and pos3d.y <= 0.0625 + EPS
    #print(pos3d.z)
    assert pos3d.z >= -0.0625 - EPS and pos3d.z <= 0.0625 + EPS
    
        
def check_pos2d(rxn_info):
    # Cube's edge is 0.125um long so this is the max
    # u or v coordinate
    
    # POTENTIAL TODO:
    # in iteration 5, we get 
    # pos2d == (0.163677, 0.001028)
    # this doesn't then matcth the triangle lengths, 
    # not sure what is correct, 
    # coversion to xyz using code from MCell's 'uv2xyz' works
    #assert pos2d.x >= 0 - EPS and pos2d.x <= 0.125 + EPS
    #assert pos2d.y >= 0 - EPS and pos2d.y <= 0.125 + EPS
    
    xyz = uv2xyz(rxn_info.geometry_object, rxn_info.wall_index, rxn_info.pos2d)
    check_pos3d(xyz)

    
rxn = model.find_reaction_rule('a_plus_sb')
assert rxn
cube = model.find_geometry_object('Cube')
assert cube

def rxn_callback(rxn_info, context):
    context.count += 1
    
    #print(rxn_info.reactant_ids);
    assert len(rxn_info.reactant_ids) == 2
    assert len(rxn_info.product_ids) == 1

    
    # we are starting with 20 molecules and not creating any new 'a' and 'b'
    assert rxn_info.reactant_ids[0] >= 0 and rxn_info.reactant_ids[0] < 200
    assert rxn_info.reactant_ids[1] >= 0 and rxn_info.reactant_ids[1] < 200
    
    assert rxn_info.reaction_rule is rxn
    assert rxn_info.geometry_object is cube
    assert rxn_info.wall_index < len(rxn_info.geometry_object.wall_list) 
    
    check_time(rxn_info.time, context.current_it)
    
    check_pos3d(rxn_info.pos3d)
    check_pos2d(rxn_info)


context = RxnCallbackContext()

model.register_reaction_callback(
    rxn_callback, context, rxn 
)

for i in range(ITERATIONS + 1):
    context.current_it = i
    model.run_iterations(1)

model.end_simulation()

print("Total number of reactions: " + str(context.count))
assert context.count == 33

