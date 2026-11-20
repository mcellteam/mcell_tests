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

# Geometry only: no volume or surface molecules are involved.

# a 2 um cube whose walls face outward, with two more vertices, 8 and 9, that
# no wall uses
box = m.GeometryObject(
    name = 'box',
    vertex_list = [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1],
                   [2, 2, 2], [-2, 0, 0]],
    wall_list = [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4],
                 [5, 1, 0], [6, 4, 0], [3, 1, 5]]
)

# a tetrahedron whose walls face outward, with one more vertex, 4, that no wall uses
tetra = m.GeometryObject(
    name = 'tetra',
    vertex_list = [[4, 0, 0], [5, 0, 0], [4, 1, 0], [4, 0, 1], [6, 6, 6]],
    wall_list = [[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3]]
)

model = m.Model()
model.add_geometry_object(box)
model.add_geometry_object(tetra)

model.config.time_step = 1e-6
model.config.total_iterations = 10
model.initialize()
model.run_iterations(10)
model.end_simulation()
