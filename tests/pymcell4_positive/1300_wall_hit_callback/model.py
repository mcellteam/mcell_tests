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

import subsystem
import instantiation

model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations_hint = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- default configuration overrides ----

# ---- add components ----

model.add_subsystem(subsystem.subsystem)
model.add_instantiation(instantiation.instantiation)

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()


# --------------- test ------------------------

# example class passed as context to the callback
class HitCount():
    def __init__(self):
        self.count = 0
        self.current_it = 0 


def check_time(time, it):
    # cannot start before iteration start
    #print("---")
    #print(time)
    #print(it)
    #print(it * TIME_STEP)
    assert time >= it * TIME_STEP
    # we are running iterations one by one therefore
    # the max time is the end of this iteration 
    assert time <= (it + 1) * TIME_STEP

def check_pos(pos3d):
    EPS = 1e-9
    # min and max coordinates from Tetrahedron_vertex_list
    assert pos3d.x >= -0.01 - EPS and pos3d.x <= 0.02 + EPS
    assert pos3d.y >= -0.02 - EPS and pos3d.y <= 0.02 + EPS
    #print(pos3d.z)
    assert pos3d.z >= -0.01 - EPS and pos3d.z <= 0.02 + EPS
        
        
tetrahedron_object = model.find_geometry_object('Tetrahedron')
assert tetrahedron_object


def wall_hit_callback(wall_hit_info, context):
    #print("Wall hit callback called")
    #print(wall_hit_info)
    context.count += 1
    
    assert wall_hit_info.geometry_object is tetrahedron_object
    assert wall_hit_info.wall_index < len(tetrahedron_object.wall_list)
    
    #print("-t")
    check_time(wall_hit_info.time, context.current_it)
    #print("-t-before")
    check_time(wall_hit_info.time_before_hit, context.current_it)
    assert wall_hit_info.time_before_hit <= wall_hit_info.time
    
    check_pos(wall_hit_info.pos3d)
    check_pos(wall_hit_info.pos3d_before_hit)
    


vm_species = model.find_species('vm')
assert vm_species
assert vm_species is subsystem.vm

context = HitCount()

# the object and species are optional, this simple test contains single
# object and species anyway 
model.register_mol_wall_hit_callback(
    wall_hit_callback, context 
)

for i in range(ITERATIONS + 1):
    context.current_it = i
    model.run_iterations(1)

model.end_simulation()

print("Total number of wall hits: " + str(context.count))
assert context.count == 36045

