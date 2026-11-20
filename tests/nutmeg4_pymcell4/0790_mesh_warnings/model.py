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

# Geometry only: no volume or surface molecules are involved. One object per
# warning of MCell4's mesh checks; warnings don't stop the run.

# a 2 um square of two walls: 4 boundary edges
plane = m.GeometryObject(
    name = 'plane',
    vertex_list = [[-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0]],
    wall_list = [[0, 1, 2], [0, 2, 3]]
)

# two tetrahedra that touch at the point (5, 0, 0), where each has its own
# vertex, 0 and 4: equal coordinates, but two watertight shells that share no
# vertex index
touching = m.GeometryObject(
    name = 'touching',
    vertex_list = [[5, 0, 0], [6, 0, 0], [5, 1, 0], [5, 0, 1], [5, 0, 0], [4, 0, 0], [5, -1, 0], [5, 0, -1]],
    wall_list = [[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3], [4, 5, 6], [4, 7, 5], [4, 6, 7], [5, 7, 6]]
)

model = m.Model()
model.add_geometry_object(plane)
model.add_geometry_object(touching)

model.config.time_step = 1e-6
model.config.total_iterations = 10
model.initialize()
model.run_iterations(10)
model.end_simulation()
