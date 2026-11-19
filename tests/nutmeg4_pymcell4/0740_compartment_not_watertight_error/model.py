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

# only volume molecules: a; there are no surface molecules
a = m.Species('a', diffusion_constant_3d = 1e-6)

# a cube without its two top walls (z = s): 4 boundary edges
CUBE_V = [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]]
CUBE_W = [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]
TOP = [5, 11]

def open_box(name, s, x0, is_compartment):
    return m.GeometryObject(
        name = name, vertex_list = [[x * s + x0, y * s, z * s] for x, y, z in CUBE_V],
        wall_list = [w for i, w in enumerate(CUBE_W) if i not in TOP], is_bngl_compartment = is_compartment)

# two BNGL compartments, EC around CP, and a counted object, all without their top walls
EC = open_box('EC', 2, 0, True)
CP = open_box('CP', 1, 0, True)
counted = open_box('counted', 1, 10, False)

model = m.Model()
model.add_species(a)
for o in [EC, CP, counted]:
    model.add_geometry_object(o)
model.add_count(m.Count(
    name = 'a_counted', expression = m.CountTerm(species_pattern = a, region = counted), file_name = 'a_counted.dat'))

model.config.time_step = 1e-6
model.config.total_iterations = 10
model.initialize()
model.run_iterations(10)
model.end_simulation()
