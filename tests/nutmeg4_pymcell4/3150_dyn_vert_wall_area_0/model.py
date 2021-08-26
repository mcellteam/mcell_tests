#!/usr/bin/env python3

# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import sys
import os
import importlib.util

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

# ---- import mcell module located in directory ----
# ---- specified by system variable MCELL_PATH  ----
MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    if os.path.exists(os.path.join(lib_path, 'mcell.so')) or \
        os.path.exists(os.path.join(lib_path, 'mcell.pyd')):
        sys.path.append(lib_path)
    else:
        print("Error: Python module mcell.so or mcell.pyd was not found in "
              "directory '" + lib_path + "' constructed from system variable "
              "MCELL_PATH.")
        sys.exit(1)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)

import mcell as m

# parameters are intentionally not imported using from ... import *
# because we may need to make changes to the module's variables
import parameters

# create main model object
model = m.Model()


a = m.Species(
    name = 'a',
    diffusion_constant_2d = 1e-8
)
model.add_species(a)

"""
b = m.Species(
    name = 'b',
    diffusion_constant_2d = 1e-8
)
model.add_species(b)
"""

box1 = m.geometry_utils.create_box('box1', 0.2)

sr1 = m.SurfaceRegion(
    name = 'sr1',
    wall_indices = [0]
)
box1.surface_regions = [sr1]
model.add_geometry_object(box1)

"""
box2 = m.geometry_utils.create_box('box2', 0.2)
sr2 = m.SurfaceRegion(
    name = 'sr2',
    wall_indices = [0]
)
box2.surface_regions = [sr2]
box2.translate((0.5, 0, 0))
model.add_geometry_object(box2)
"""

rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = a,
    region = sr1,
    number_to_release = 1
)
model.add_release_site(rel_a)

"""
rel_b = m.ReleaseSite(
    name = 'rel_b',
    complex = b,
    region = sr2,
    number_to_release = 1
)
model.add_release_site(rel_b)
"""

viz_output = m.VizOutput()
model.add_viz_output(viz_output)

# ---- configuration ----

model.config.time_step = parameters.TIME_STEP
model.config.seed = parameters.SEED
model.config.total_iterations = parameters.ITERATIONS

model.notifications.rxn_and_species_report = False

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.5

# ---- default configuration overrides ----

# ---- add components ----

model.initialize()

if parameters.DUMP:
    model.dump_internal_state()

model.export_data_model()

# release molecules
model.run_iterations(1)

ida = 0
idb = 1

# check species
ma = model.get_molecule(ida)
assert model.get_species_name(ma.species_id) == 'a'
#mb = model.get_molecule(idb)
#assert model.get_species_name(mb.species_id) == 'b'

# pair molecules
#model.pair_molecules(ida, idb)


for iter in range (1, 10):
    print("Iteration:", iter)

    model.export_data_model()
    
    # move with vertices
    for i in range(0, 3):
        print("Moving vertex: ", box1.wall_list[0][i] ) 
        #model.add_vertex_move(box1, box1.wall_list[0][i], (0.02, 0.02, 0))
        model.add_vertex_move(box1, box1.wall_list[0][i], (0.05, 0.05, 0))
    model.apply_vertex_moves()
    
    print(box1.__str__(True))
    
    model.run_iterations(1)


# check that vertices of box2 were moved (ther API side)

model.end_simulation()
