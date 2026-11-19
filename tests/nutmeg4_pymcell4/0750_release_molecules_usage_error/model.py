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

CUBE_V = [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]]
CUBE_W = [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]
TOP = [5, 11] # the two walls at z = 1

def vertices(x0):
    return [[x + x0, y, z] for x, y, z in CUBE_V]

# a 2 um cube, the same cube without its top walls (4 boundary edges), and the
# cube with its walls reversed, so that they face inward
cube = m.GeometryObject(name = 'cube', vertex_list = vertices(0), wall_list = CUBE_W)
open_box = m.GeometryObject(
    name = 'open_box', vertex_list = vertices(5), wall_list = [w for i, w in enumerate(CUBE_W) if i not in TOP])
inside_out = m.GeometryObject(
    name = 'inside_out', vertex_list = vertices(10), wall_list = [[w[0], w[2], w[1]] for w in CUBE_W])

model = m.Model()
model.add_species(a)
for o in [cube, open_box, inside_out]:
    model.add_geometry_object(o)
model.config.time_step = 1e-6
model.config.total_iterations = 10
model.initialize()
model.run_iterations(1)
now = 1e-6 # the start of iteration 1

# each release that the object's mesh doesn't allow raises a ValueError and
# releases nothing; the model goes on
for rel in [
        m.ReleaseSite(name = 'rel_open_box', complex = a, region = open_box, number_to_release = 100, release_time = now),
        m.ReleaseSite(name = 'rel_inside_out', complex = a, region = inside_out, concentration = 1e-6, release_time = now)]:
    try:
        model.release_molecules(rel)
        print('no error for ' + rel.name, file = sys.stderr)
    except ValueError as e:
        print('ValueError from ' + rel.name + ': ' + str(e), file = sys.stderr)
assert len(model.get_molecule_ids()) == 0

# a release into the watertight cube works
model.release_molecules(m.ReleaseSite(name = 'rel_cube', complex = a, region = cube, number_to_release = 10, release_time = now))
assert len(model.get_molecule_ids()) == 10

model.run_iterations(9)
model.end_simulation()
