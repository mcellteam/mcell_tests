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

SEED = 1
ITERATIONS = 20 

model = m.Model()

# subsystem
species_a = m.Species(
    name = 'a',
    diffusion_constant_3d = 1e-06
)

species_b = m.Species(
    name = 'b',
    diffusion_constant_3d = 1e-06
)

subsystem = m.Subsystem()
model.add_species(species_a)
model.add_species(species_b)


# geometry
box_inner = m.geometry_utils.create_box('box_inner', 0.3) 
box_outer = m.geometry_utils.create_box('box_outer', 0.6)

model.add_geometry_object(box_inner)
model.add_geometry_object(box_outer)

# instantiation 
rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = m.Complex('a'),
    region = box_inner,
    number_to_release = 10
)

rel_b = m.ReleaseSite(
    name = 'rel_b',
    complex = m.Complex('b'),
    region = box_outer - box_inner,
    number_to_release = 10
)

model.add_release_site(rel_a)
model.add_release_site(rel_b)

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5


# --------------- test ------------------------

# example class passed as context to the callback
class HitCount():
    def __init__(self):
        self.count = 0
        self.current_it = 0 
        self.expected_species = None


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

def check_pos_inner(pos3d):
    EPS = 1e-9
    # min and max coordinates 
    assert pos3d[0] >= -0.3 - EPS and pos3d[0] <= 0.3 + EPS
    assert pos3d[1] >= -0.3 - EPS and pos3d[1] <= 0.3 + EPS
    assert pos3d[2] >= -0.3 - EPS and pos3d[2] <= 0.3 + EPS
        

def check_pos_outer(pos3d):
    EPS = 1e-9
    # min and max coordinates 
    assert pos3d[0] >= -0.6 - EPS and pos3d[0] <= 0.6 + EPS
    assert pos3d[1] >= -0.6 - EPS and pos3d[1] <= 0.6 + EPS
    assert pos3d[2] >= -0.6 - EPS and pos3d[2] <= 0.6 + EPS
        

def check_times(wall_hit_info, context):
    check_time(wall_hit_info.time, context.current_it)
    check_time(wall_hit_info.time_before_hit, context.current_it)
    assert wall_hit_info.time_before_hit <= wall_hit_info.time

def check_inner(wall_hit_info, context):
    assert wall_hit_info.geometry_object is box_inner
    assert wall_hit_info.wall_index < len(box_inner.wall_list)
    
    check_pos_inner(wall_hit_info.pos3d)
    check_pos_inner(wall_hit_info.pos3d_before_hit)
    
    check_times(wall_hit_info, context)
    
    
def check_outer(wall_hit_info, context):
    assert wall_hit_info.geometry_object is box_outer
    assert wall_hit_info.wall_index < len(box_outer.wall_list)
    
    check_pos_outer(wall_hit_info.pos3d)
    check_pos_outer(wall_hit_info.pos3d_before_hit)
    
    check_times(wall_hit_info, context)
        
        
def check_expected_species(wall_hit_info, context):
    if not context.expected_species:
        return
         
    # molecule id to species
    mol = model.get_molecule(wall_hit_info.molecule_id)
    species_name = model.get_species_name(mol.species_id)

    assert context.expected_species.to_bngl_str() == species_name 


def wall_hit_callback_inner(wall_hit_info, context):
    context.count += 1
    check_expected_species(wall_hit_info, context)
    check_inner(wall_hit_info, context)
        
    
def wall_hit_callback_outer(wall_hit_info, context):
    context.count += 1
    check_expected_species(wall_hit_info, context)
    check_outer(wall_hit_info, context)
    
def wall_hit_callback_any(wall_hit_info, context):
    context.count += 1
    check_expected_species(wall_hit_info, context)
    check_pos_outer(wall_hit_info.pos3d)
    check_pos_outer(wall_hit_info.pos3d_before_hit)

# callbacks must be registered after initialization
model.initialize() 



context_inner_a = HitCount()
context_inner_a.expected_species = species_a
model.register_mol_wall_hit_callback(
    wall_hit_callback_inner, context_inner_a, box_inner, species_a 
)

context_inner_b = HitCount()
context_inner_b.expected_species = species_b
model.register_mol_wall_hit_callback(
    wall_hit_callback_inner, context_inner_b, box_inner, species_b 
)

context_inner_any = HitCount()
model.register_mol_wall_hit_callback(
    wall_hit_callback_inner, context_inner_any, box_inner 
)

context_outer_a = HitCount()
context_outer_a.expected_species = species_a
model.register_mol_wall_hit_callback(
    wall_hit_callback_outer, context_outer_a, box_outer, species_a 
)

context_outer_b = HitCount()
context_outer_b.expected_species = species_b
model.register_mol_wall_hit_callback(
    wall_hit_callback_outer, context_outer_b, box_outer, species_b 
)

context_any_a = HitCount()
context_any_a.expected_species = species_a
model.register_mol_wall_hit_callback(
    wall_hit_callback_any, context_any_a, species = species_a
)

context_any = HitCount()
model.register_mol_wall_hit_callback(
    wall_hit_callback_any, context_any
)

all_contexts = [
    context_inner_a, context_inner_b, context_inner_any,
    context_outer_a, context_outer_b, 
    context_any_a, context_any
]

# ---- initialization and execution ----

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

for i in range(ITERATIONS):
    for ctx in all_contexts:
        ctx.current_it = i
    model.run_iterations(1)
    
model.end_simulation()

"""
print("assert context_inner_a.count == " + str(context_inner_a.count))
print("assert context_inner_b.count  == " + str(context_inner_b.count))
print("assert context_inner_any.count == " + str(context_inner_any.count))
print("assert context_outer_a.count == " + str(context_outer_a.count))
print("assert context_outer_b.count == " + str(context_outer_b.count))
print("assert context_any_a.count == " + str(context_any_a.count))
print("assert context_any.count == " + str(context_any.count))
"""

assert context_outer_a.count == 0
assert context_any_a.count == context_inner_a.count
assert context_inner_any.count == context_inner_a.count + context_inner_b.count
assert context_any.count == context_inner_any.count + context_outer_b.count 

assert context_inner_a.count == 28
assert context_inner_b.count  == 2
assert context_inner_any.count == 30
assert context_outer_a.count == 0
assert context_outer_b.count == 23
assert context_any_a.count == 28
assert context_any.count == 53



