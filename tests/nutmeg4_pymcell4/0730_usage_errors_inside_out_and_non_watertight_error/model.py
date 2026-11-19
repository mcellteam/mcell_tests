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

# a 2 um cube whose walls face outward, centered at x0
CUBE_V = [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]]
CUBE_W = [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]
TOP = [5, 11] # the two walls at z = 1

def vertices(x0):
    return [[x + x0, y, z] for x, y, z in CUBE_V]

# its walls reversed, so that they face inward
inside_out = m.GeometryObject(
    name = 'inside_out', vertex_list = vertices(0), wall_list = [[w[0], w[2], w[1]] for w in CUBE_W])
# without its top walls: 4 boundary edges
open_box = m.GeometryObject(
    name = 'open_box', vertex_list = vertices(5), wall_list = [w for i, w in enumerate(CUBE_W) if i not in TOP])
# a BNGL compartment whose walls face inward
CP = m.GeometryObject(
    name = 'CP', vertex_list = vertices(10), wall_list = [[w[0], w[2], w[1]] for w in CUBE_W],
    is_bngl_compartment = True)

model = m.Model()
model.add_species(a)
for o in [inside_out, open_box, CP]:
    model.add_geometry_object(o)

# inside_out: counted, and released into by concentration
model.add_count(m.Count(
    name = 'a_inside_out', expression = m.CountTerm(species_pattern = a, region = inside_out), file_name = 'a_inside_out.dat'))
model.add_release_site(m.ReleaseSite(name = 'rel_conc', complex = a, region = inside_out, concentration = 1e-6))
# open_box: counted, released into by number, and removed from by a negative concentration
model.add_count(m.Count(
    name = 'a_open_box', expression = m.CountTerm(species_pattern = a, region = open_box), file_name = 'a_open_box.dat'))
model.add_release_site(m.ReleaseSite(name = 'rel_number', complex = a, region = open_box, number_to_release = 100))
model.add_release_site(m.ReleaseSite(
    name = 'rel_remove', complex = a, region = open_box, concentration = -1e-6, release_time = 5e-6))

model.config.time_step = 1e-6
model.config.total_iterations = 10
model.initialize()
model.run_iterations(10)
model.end_simulation()
