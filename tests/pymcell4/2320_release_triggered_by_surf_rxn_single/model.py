#!/usr/bin/env python3

import sys
import os
import numpy as np
import math
from scipy.spatial.transform import Rotation

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
def cmp_eq(a, b):
    return abs(a - b) < 1e-8
    
    
def rotate_about_normal(normal, displacement):
    # from MCell3 function reaction_wizardry
    # Set up transform that will translate and then rotate Z axis to align
    # with surface normal 
    axis = m.Vec3(1, 0, 0)
    cos_theta = normal.z
    if cmp_eq(cos_theta, -1.0):
        degrees = 180.0
    else:
        axis.x = -normal.y
        axis.y = normal.x
        axis.z = 0
        
        degrees = math.acos(cos_theta) * 180.0 / math.pi  

    # from https://www.kite.com/python/answers/how-to-rotate-a-3d-vector-about-an-axis-in-python
    rotation_radians = np.radians(degrees)
    rotation_vector = rotation_radians * np.array(axis.to_list())
    rotation = Rotation.from_rotvec(rotation_vector)
    res = rotation.apply(displacement.to_list())
    
    return m.Vec3(res[0], res[1], res[2])  

def rxn_callback(rxn_info, model):
    assert rxn_info.type == m.ReactionType.VOLUME_SURFACE
    
    # we will be moving in the direction
    # of the wall's normal 
    w = model.get_wall(rxn_info.geometry_object, rxn_info.wall_index)
    
    # MCell3 (reference model) mdl_mcell3/2310_release_triggered_by_surf_rxn_single
    # computes position like this:
    pos = rxn_info.pos3d + rotate_about_normal(w.unit_normal, m.Vec3(-0.005, -0.005, -0.005))
    
    # it is also possible to move it in the direction of the unit normal
    #pos = rxn_info.pos3d + w.unit_normal * m.Vec3(-0.005, -0.005, -0.005)
    
    # release molecules
    rel_a = m.ReleaseSite(
        name = 'rel_c',
        complex = subsystem.c.inst(),
        shape = m.Shape.SPHERICAL,
        location = pos,
        site_diameter = 0,
        number_to_release = 10,
        release_time = rxn_info.time
    )
    model.release_molecules(rel_a)
    
    
model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

# sending model as context
model.register_reaction_callback(
    rxn_callback, model, subsystem.react_a_and_b 
)

model.run_iterations(ITERATIONS)
model.end_simulation()
