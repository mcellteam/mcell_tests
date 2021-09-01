#!/usr/bin/env python3
"""
This command runs Blender for visualization
~/mcell4_release/mcell_tools/work/bundle_install/Blender-2.79-CellBlender/my_blender -P ~/mcell4_release/mcell_tools/work/bundle_install/Blender-2.79-CellBlender/2.79/scripts/addons/cellblender/developer_utilities/mol_viz_scripts/viz_mcell_run.py -- viz_data/seed_00001/
"""
import sys
import os
import random as rnd
import numpy as np

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m


SEED = 1
ITERATIONS = 600
TIME_STEP = 1.00000000e-06
DUMP = False
EXPORT_DATA_MODEL = False


if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])

from geometry import *

model = m.Model()

# ---- add components ----

# add geometry
Sphere1.is_bngl_compartment = True 
Sphere1.surface_compartment_name = 'PM1' 
Sphere2.is_bngl_compartment = True 
Sphere2.surface_compartment_name = 'PM2'

model.add_geometry_object(Sphere1)
model.add_geometry_object(Sphere2)


# load information on species and on our reaction 
model.load_bngl('model.bngl')
    
# define reflective surface classes for our regions - same as in the lipid raft example so that 
# our molecules don't diffuse away for the regions where the 'cells' touch
# when using the surface class, the molecules weirdly agreggate at its boundary, 
# this is probably something to be checked. 
# however in reality the whole object won't more so quickly so 
# this might not be an issue
lipid_raft_A = m.SurfaceClass(
    name = 'lipid_raft_A',
    type = m.SurfacePropertyType.REFLECTIVE,
    affected_complex_pattern = m.Complex('A')
)

lipid_raft_B = m.SurfaceClass(
    name = 'lipid_raft_B',
    type = m.SurfacePropertyType.REFLECTIVE,
    affected_complex_pattern = m.Complex('B')
)
model.add_surface_class(lipid_raft_A)
model.add_surface_class(lipid_raft_B)
    
Sphere1_right.surface_class = lipid_raft_A
Sphere2_left.surface_class = lipid_raft_B   


# release molecules in specified regions
rel_A = m.ReleaseSite(
    name = 'rel_A',
    complex = m.Complex('A', orientation = m.Orientation.UP),
    region = Sphere1_right,
    number_to_release = 350
)

rel_B = m.ReleaseSite(
    name = 'rel_B',
    complex = m.Complex('B', orientation = m.Orientation.UP),
    region = Sphere2_left,
    number_to_release = 350
)

model.add_release_site(rel_A)
model.add_release_site(rel_B)


# must be 1 for visualization to work correctly (for now)
VIZ_FREQUENCY = 1
    
# viz output to visualize molecules
viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = VIZ_FREQUENCY
)

model.add_viz_output(viz_output)

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5


# ---- initialization and execution ----


# we need to set an extra flag for our reaction to specify that it can 
# occur in an intermembrane fashion
# this reaction cuases A+B to become C+D and in this reaction's callback we 
# fix the walls so they cannot move
rxn_A_plus_B = model.find_reaction_rule('A_plus_B')
assert rxn_A_plus_B
rxn_A_plus_B.is_intermembrane_surface_reaction = True

# get ReactionRule objects for the 'unbinding' reactions where  
rxn_C_to_E = model.find_reaction_rule('C_to_E')
assert rxn_C_to_E

rxn_D_to_B = model.find_reaction_rule('D_to_B')
assert rxn_D_to_B


model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()


def print_molecule_info(model, id, msg):
    m = model.get_molecule(id)
    assert m.id == id 
    s = model.get_species_name(m.species_id)
    
    print("  " + msg + " (" + str(m.id) + " - " + s + "): " + m.geometry_object.name + ":" + str(m.wall_index))


def a_plus_b_callback(rxn_info, model):
    assert rxn_info.type == m.ReactionType.SURFACE_SURFACE 
    
    assert len(rxn_info.reactant_ids) == 2
    
    print("** Binding of membrane through reaction A + B -> C + D (" + 
          str(rxn_info.product_ids[0]) + ")")
     
    print_molecule_info(model, rxn_info.reactant_ids[0], "reactant 1")
    print_molecule_info(model, rxn_info.reactant_ids[1], "reactant 2")
    
    # block walls - by setting 'is_movable' model that they are held together
    
    # get the first reactant and block its wall, reac1 may be either A or B
    reac1 = model.get_molecule(rxn_info.reactant_ids[0])
    assert reac1.type == m.MoleculeType.SURFACE

    # tell MCell that the two molecules are paired and that when 
    # a wall with one molecule is moved, the second wall is moved as well 
    model.pair_molecules(rxn_info.product_ids[0], rxn_info.product_ids[1])
    
    # debug printout on locations of products
    print_molecule_info(model, rxn_info.product_ids[0], "product 1")
    print_molecule_info(model, rxn_info.product_ids[1], "product 2")

    

def c_to_e_callback(rxn_info, model):
    print("** Unbinding of membrane through reaction C -> A and D -> B (" + 
          str(rxn_info.reactant_ids[0]) + ")")
    
    # this callback is called when a unimolecular reaction of C occurs
    
    assert len(rxn_info.reactant_ids) == 1
    reactant_C_id = rxn_info.reactant_ids[0] 
    
    # we did not start with any C molecules, the only ones in our system are created 
    # through the A + B -> C + D reaction, therefore C must be a paired molecule
    # and we get the original D with get_paired_molecule
    
    reactant_D_id = model.get_paired_molecule(reactant_C_id)
    assert reactant_D_id != m.ID_INVALID
    
    print_molecule_info(model, reactant_C_id, "reactant 1")
    print_molecule_info(model, reactant_D_id, "reactant 2")
    
    # and change D back to B
    products = model.run_reaction(rxn_D_to_B, [reactant_D_id], rxn_info.time)
    assert len(products) == 1
    
    print("  changed D to B, resulting molecule id of B is " + str(products[0]))
    
    print_molecule_info(model, rxn_info.product_ids[0], "product 1")
    print_molecule_info(model, products[0], "product 2")


# register reaction callback(s)
model.register_reaction_callback(
    a_plus_b_callback,
    model, 
    rxn_A_plus_B 
)

model.register_reaction_callback(
    c_to_e_callback, 
    model, 
    rxn_C_to_E
)

# and run simulation    
for i in range(ITERATIONS):
    print("IT", i)
    
    # dump datamodel every N iterations
    if i % VIZ_FREQUENCY == 0: 
        model.export_viz_data_model()
            
    for k in range(len(Sphere1_vertex_list)):
        # first move our sphere towards, then want, then move it back 
        if i < 100:
            dir = 1
        elif i >= 100 and i < 200:
            dir = 0            
        else:
            dir = -0.5
        model.add_vertex_move(Sphere1, k, (0, dir * 0.01, 0))

    model.apply_vertex_moves(randomize_order=False)
            
    model.run_iterations(1)
    

model.end_simulation()
