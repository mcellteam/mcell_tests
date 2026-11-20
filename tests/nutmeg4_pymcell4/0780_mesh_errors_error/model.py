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
# error of MCell4's mesh checks; each object lies 5 um further along x.

# a 2 um cube whose walls face outward
CUBE_V = [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]]
CUBE_W = [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4],
          [5, 1, 0], [6, 4, 0], [3, 1, 5]]

# the cube, but wall 5 uses vertex 3 twice
repeated = m.GeometryObject(
    name = 'repeated',
    vertex_list = CUBE_V,
    wall_list = [[3, 5, 3] if i == 5 else w for i, w in enumerate(CUBE_W)]
)

# one wall and its reversed copy: two walls on the same three vertices
duplicate = m.GeometryObject(
    name = 'duplicate',
    vertex_list = [[5, 0, 0], [6, 0, 0], [5, 1, 0]],
    wall_list = [[0, 1, 2], [2, 1, 0]]
)

# a 2 um square and a wall along its edge y = -1, through vertex 4 at the edge's
# middle: wall 2 has zero area
zero = m.GeometryObject(
    name = 'zero',
    vertex_list = [[9, -1, 0], [11, -1, 0], [11, 1, 0], [9, 1, 0], [10, -1, 0]],
    wall_list = [[0, 1, 2], [0, 2, 3], [0, 4, 1]]
)

# three walls on the edge 0-1, like the pages of a book
book = m.GeometryObject(
    name = 'book',
    vertex_list = [[15, 0, 0], [15, 0, 1], [16, 0, 0], [14, 0, 0], [15, 1, 0]],
    wall_list = [[0, 1, 2], [1, 0, 3], [0, 1, 4]]
)

# two walls that share only vertex 0
bowtie = m.GeometryObject(
    name = 'bowtie',
    vertex_list = [[20, 0, 0], [21, 0, 0], [21, 1, 0], [19, 0, 0], [19, -1, 0]],
    wall_list = [[0, 1, 2], [0, 3, 4]]
)

# the cube with wall 4 reversed: it runs along its three edges in the same
# direction as its neighbours 0, 1 and 10
flipped = m.GeometryObject(
    name = 'flipped',
    vertex_list = [[x + 25, y, z] for x, y, z in CUBE_V],
    wall_list = [[2, 0, 6] if i == 4 else w for i, w in enumerate(CUBE_W)]
)

# a square whose lists and surface region are changed through the setters, after
# the constructor has checked them: vertex 4 has two coordinates, wall 1 has two
# vertex indices, wall 3 has the index 9 (out of range), wall 4 uses vertex 1
# twice, and region r has the wall indices 7 and -1 (out of range for 5 walls)
bad = m.GeometryObject(
    name = 'bad',
    vertex_list = [[30, 0, 0], [31, 0, 0], [31, 1, 0], [30, 1, 0]],
    wall_list = [[0, 1, 2], [0, 2, 3]],
    surface_regions = [m.SurfaceRegion(name = 'r', wall_indices = [0])]
)
bad.vertex_list = [[30, 0, 0], [31, 0, 0], [31, 1, 0], [30, 1, 0], [30.5, 0.5]]
bad.wall_list = [[0, 1, 2], [0, 2], [0, 2, 3], [0, 9, 3], [1, 1, 2]]
bad.surface_regions[0].wall_indices = [0, 7, -1, 7]

model = m.Model()
for o in [repeated, duplicate, zero, book, bowtie, flipped, bad]:
    model.add_geometry_object(o)

model.config.time_step = 1e-6
model.config.total_iterations = 10
model.initialize()
model.run_iterations(10)
model.end_simulation()
