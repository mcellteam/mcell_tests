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
ITERATIONS = 100
TIME_STEP = 1.00000000e-06
DUMP = False
EXPORT_DATA_MODEL = False


if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])

from geometry import *
from observables import *

model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- add components ----

# TODO viz in cellblender without any molecules does not work yet
a = m.Species(
    name = 'a',
    diffusion_constant_3d = 1e-6
)
model.add_species(a)
rel = m.ReleaseSite(
    name = 'rel',
    complex = a,
    shape = m.Shape.SPHERICAL,
    location = (0, 0, 0),
    site_diameter = 0,
    number_to_release = 1
)
model.add_release_site(rel)

model.add_geometry_object(Sphere1)
model.add_geometry_object(Sphere2)
model.add_observables(observables)

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()


def print_wall_hit_info(wall_wall_hits):
    for info in wall_wall_hits:
        print(info.wall1.geometry_object.name + ":" + str(info.wall1.wall_index) + " - " + 
              info.wall2.geometry_object.name + ":" + str(info.wall2.wall_index))

# counts both hits that occured when a moved vertex hit the second object and 
# when the second's object vertex would get inside into the moved object 
num_hits = 0
            
for i in range(ITERATIONS):
    
    # dump datamodel every N iterations
    model.export_viz_data_model()
            
    for k in range(len(Sphere1_vertex_list)):
        model.add_vertex_move(Sphere1, k, (0.01, 0.01, 0.01))

    wall_wall_hits = model.apply_vertex_moves(collect_wall_wall_hits=True, randomize_order=False)
    #print_wall_hit_info(wall_wall_hits)
    num_hits += len(wall_wall_hits)
            
    # vertex must not move into the box 
    v1 = model.get_vertex(Sphere1, 90)
    assert v1.x < 1.48 # 1.475210 was the final position
                
    model.run_iterations(1)
    

model.end_simulation()

print(num_hits)
assert num_hits == 35783
