#!/usr/bin/env python3

import sys
import os
import numpy as np
import math
#from scipy.spatial.transform import Rotation

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

model.config.partition_dimension = 20.02
model.config.subpartition_dimension = 2.002

# ---- default configuration overrides ----


# ---- add components ----

model.add_subsystem(subsystem.subsystem)
model.add_instantiation(instantiation.instantiation)
model.add_observables(observables.observables)

# ---- initialization and execution ----
def cmp_eq(a, b):
    return abs(a - b) < 1e-8
    
"""
# implementation that uses scipy.spatial.transform import Rotation
def rotate_about_normal_scipy(normal, displacement):
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
"""

# implementation that does not use scipy.spatial.transform 
def rotate_about_normal(normal, displacement):
    
    axis = m.Vec3(1, 0, 0)
    cos_theta = normal[2]
    if cmp_eq(cos_theta, -1.0):
        angle = 180.0
    else:
        axis.x = -normal[1]
        axis.y = normal[0]
        axis.z = 0
        
        angle = math.acos(cos_theta) * 180.0 / math.pi  
    
    r1 = np.empty([4, 4])    
    r2 = np.empty([4, 4])
    r3 = np.empty([4, 4]) 
    
    np_axis = np.array(axis.to_list())
    np_axis = np_axis/np.linalg.norm(np_axis)
    a = np_axis[0];
    b = np_axis[1];
    c = np_axis[2];
    v = math.sqrt(b * b + c * c);
  
    r1[0][0] = 1;
    r1[0][1] = 0;
    r1[0][2] = 0;
    r1[0][3] = 0;
    r1[1][0] = 0;
    r1[1][1] = 1;
    r1[1][2] = 0;
    r1[1][3] = 0;
    r1[2][0] = 0;
    r1[2][1] = 0;
    r1[2][2] = 1;
    r1[2][3] = 0;
    r1[3][0] = 0;
    r1[3][1] = 0;
    r1[3][2] = 0;
    r1[3][3] = 1;
    
    if v != 0.0:
        r1[1][1] = c / v;
        r1[1][2] = b / v;
        r1[2][1] = -b / v;
        r1[2][2] = c / v;
  
    r2[0][0] = v;
    r2[0][1] = 0;
    r2[0][2] = a;
    r2[0][3] = 0;
    r2[1][0] = 0;
    r2[1][1] = 1;
    r2[1][2] = 0;
    r2[1][3] = 0;
    r2[2][0] = -a;
    r2[2][1] = 0;
    r2[2][2] = v;
    r2[2][3] = 0;
    r2[3][0] = 0;
    r2[3][1] = 0;
    r2[3][2] = 0;
    r2[3][3] = 1;
    
    rad = math.pi / 180.0;
    r3[0][0] = math.cos(angle * rad);
    r3[0][1] = math.sin(angle * rad);
    r3[0][2] = 0;
    r3[0][3] = 0;
    r3[1][0] = -math.sin(angle * rad);
    r3[1][1] = math.cos(angle * rad);
    r3[1][2] = 0;
    r3[1][3] = 0;
    r3[2][0] = 0;
    r3[2][1] = 0;
    r3[2][2] = 1;
    r3[2][3] = 0;
    r3[3][0] = 0;
    r3[3][1] = 0;
    r3[3][2] = 0;
    r3[3][3] = 1;
    
    #om = r1.dot(r2)
    om = np.matmul(r1, r2)
    om = np.matmul(om, r3)
    
    r2[0][2] = -a;
    r2[2][0] = a;
  
    if v != 0:
        r1[1][2] = -b / v;
        r1[2][1] = b / v;
    
    om = np.matmul(om, r2)
    om = np.matmul(om, r1)
    
    l = displacement.to_list()
    l.append(1.0)
    #print(l)
    np_displ = np.array(l)
    #print(np_displ)
    res = np.matmul(np_displ, om)
    
    return [res[0], res[1], res[2]]  

    
def rxn_callback(rxn_info, model):
    assert rxn_info.type == m.ReactionType.VOLUME_SURFACE
    
    # we will be moving in the direction
    # of the wall's normal 
    w = model.get_wall(rxn_info.geometry_object, rxn_info.wall_index)
    
    # MCell3 (reference model) mdl_mcell3/2310_release_triggered_by_surf_rxn_single
    # computes position like this:
    
    pos = np.array(rxn_info.pos3d) + np.array(rotate_about_normal(w.unit_normal, m.Vec3(-0.005, -0.005, -0.005)))
    
    # it is also possible to move it in the direction of the unit normal
    #pos = rxn_info.pos3d + w.unit_normal * m.Vec3(-0.005, -0.005, -0.005)
    
    # release molecules
    rel_a = m.ReleaseSite(
        name = 'rel_c',
        complex = subsystem.c.inst(),
        shape = m.Shape.SPHERICAL,
        location = pos.tolist(),
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
