# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

# ---- Cube ----
# originally: 0.806008994579315
Cube_vertex_list = [
    [-0.125, -0.125, -0.125], 
    [-0.125, -0.125, 0.125], 
    [-0.125, 0.125, -0.125], 
    [-0.125, 0.125, 0.125], 
    [0.125, -0.125, -0.125], 
    [0.125, -0.125, 0.125], 
    [0.125, 0.125, -0.125], 
    [0.125, 0.125, 0.125]
] # Cube_vertex_list

Cube_wall_list = [
    [3, 0, 1], 
    [7, 2, 3], 
    [5, 6, 7], 
    [1, 4, 5], 
    [2, 4, 0], 
    [7, 1, 5], 
    [3, 2, 0], 
    [7, 6, 2], 
    [5, 4, 6], 
    [1, 0, 4], 
    [2, 6, 4], 
    [7, 3, 1]
] # Cube_wall_list

Cube = m.GeometryObject(
    name = 'Cube',
    vertex_list = Cube_vertex_list,
    wall_list = Cube_wall_list,
    surface_regions = []
)
# ^^^^ Cube ^^^^


