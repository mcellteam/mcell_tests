# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

# ---- Cube1 ----
Cube1_vertex_list = [
    [1, -1, -1], # 0
    [1, -1, 1],  # 1
    [1, 1, -1],  # 2
    [1, 1, 1],   # 3
    [3, -1, -1],
    [3, -1, 1], 
    [3, 1, -1], 
    [3, 1, 1]
] # Cube1_vertex_list

Cube1_wall_list = [
    [1, 2, 0], # 0 
    [3, 6, 2], # 1
    [7, 4, 6], # 2
    [5, 0, 4], # 3
    [6, 0, 2], # 4
    [3, 5, 7], # 5
    [1, 3, 2], # 6 x
    [3, 7, 6], # 7
    [7, 5, 4], # 8
    [5, 1, 0], # 9
    [6, 4, 0], # 0
    [3, 1, 5]
] # Cube1_wall_list

Cube1 = m.GeometryObject(
    name = 'Cube1',
    vertex_list = Cube1_vertex_list,
    wall_list = Cube1_wall_list,
    surface_regions = []
)
# ^^^^ Cube1 ^^^^


# ---- Cube2 ----
Cube2_vertex_list = [
    [-1, 1, 1], 
    [-1, 1, -1], 
    [-1, -1, 1], 
    [-1, -1, -1], 
    [1, 1, 1], 
    [1, 1, -1], 
    [1, -1, 1], 
    [1, -1, -1]
] # Cube2_vertex_list

Cube2_wall_list = [
    [1, 2, 0], 
    [3, 6, 2], 
    [5, 0, 4], 
    [6, 0, 2], 
    [3, 5, 7], 
    [1, 3, 2], 
    [3, 7, 6], 
    [5, 1, 0], 
    [6, 4, 0], 
    [3, 1, 5], 
    [6, 7, 5], 
    [5, 4, 6]
] # Cube2_wall_list


Cube2 = m.GeometryObject(
    name = 'Cube2',
    vertex_list = Cube2_vertex_list,
    wall_list = Cube2_wall_list,
    surface_regions = []
)
# ^^^^ Cube2 ^^^^


