# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

# ---- Cube1 ----
Cube1_vertex_list = [
    [1, -1, -1], 
    [1, -1, 1], 
    [1, 1, -1], 
    [1, 1, 1], 
    [3, -1, -1], 
    [3, -1, 1], 
    [3, 1, -1], 
    [3, 1, 1]
] # Cube1_vertex_list

Cube1_wall_list = [
    [1, 2, 0], 
    [3, 6, 2], 
    [7, 4, 6], 
    [5, 0, 4], 
    [6, 0, 2], 
    [3, 5, 7], 
    [1, 3, 2], 
    [3, 7, 6], 
    [7, 5, 4], 
    [5, 1, 0], 
    [6, 4, 0], 
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


# ---- Outer ----
Outer_vertex_list = [
    [1, 1, 1], 
    [3, -1, -1], 
    [3, -1, 1], 
    [3, 1, -1], 
    [3, 1, 1], 
    [-1, 1, -1], 
    [-1, -1, 1], 
    [-1, -1, -1], 
    [1, -1, -1], 
    [-1, 1, 1], 
    [1, -1, 1], 
    [1, 1, -1]
] # Outer_vertex_list

Outer_wall_list = [
    [0, 3, 11], 
    [4, 1, 3], 
    [2, 8, 1], 
    [3, 8, 11], 
    [0, 2, 4], 
    [0, 4, 3], 
    [4, 2, 1], 
    [2, 10, 8], 
    [3, 1, 8], 
    [0, 10, 2], 
    [5, 6, 9], 
    [7, 10, 6], 
    [11, 9, 0], 
    [10, 9, 6], 
    [7, 11, 8], 
    [7, 8, 10], 
    [11, 5, 9], 
    [10, 0, 9], 
    [7, 5, 11], 
    #[5, 7, 6]   # commented out
] # Outer_wall_list

Outer = m.GeometryObject(
    name = 'Outer',
    vertex_list = Outer_vertex_list,
    wall_list = Outer_wall_list,
    surface_regions = []
)
# ^^^^ Outer ^^^^


