#!/usr/bin/env python3

import sys
import os
import copy
import numpy as np

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

ITERATIONS = 10

from geometry import *
from observables import *

model = m.Model()

model.add_observables(observables)

# TODO viz in cellblender without any molecules does not work yet
a = m.Species(
    name = 'a',
    diffusion_constant_3d = 0
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


Tetrahedron.translate((-0.2, 0, 0))

model.add_geometry_object(Tetrahedron)

Box = m.geometry_utils.create_box(
    'Box', 0.2
)
model.add_geometry_object(Box)
    
model.config.total_iterations = ITERATIONS
    
model.initialize()

def print_wall_hit_info(wall_wall_hits):
    for info in wall_wall_hits:
        print(info.wall1.geometry_object.name + ":" + str(info.wall1.wall_index) + " - " + 
              info.wall2.geometry_object.name + ":" + str(info.wall2.wall_index))

for i in range(ITERATIONS + 1):
    model.export_viz_data_model()
            
    for k in range(len(Tetrahedron_vertex_list) - 1): # not moving with the last vertex
        model.add_vertex_move(Tetrahedron, k, (0.02, 0, 0))
        
    wall_wall_hits = model.apply_vertex_moves(collect_wall_wall_hits=True, randomize_order=False)
    print_wall_hit_info(wall_wall_hits)
    
    if i == 3:
        assert len(wall_wall_hits) == 3
        # checking depends on Tetrahedron having internal object id 0 and Box id 1
         
        assert wall_wall_hits[2].wall1.geometry_object is Tetrahedron
        assert wall_wall_hits[2].wall1.wall_index == 3
        assert wall_wall_hits[2].wall2.geometry_object == Box
        assert wall_wall_hits[2].wall2.wall_index == 0
    
    model.run_iterations(1)
    

model.end_simulation()


