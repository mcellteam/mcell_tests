# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

# ---- Cube ----
Cube_vertex_list = [
    [-0.25, -0.25, -0.25], 
    [-0.25, -0.25, 0.25], 
    [-0.25, 0.25, -0.25], 
    [-0.25, 0.25, 0.25], 
    [0.25, -0.25, -0.25], 
    [0.25, -0.25, 0.25], 
    [0.25, 0.25, -0.25], 
    [0.25, 0.25, 0.25]
] # Cube_vertex_list

Cube_wall_list = [
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
] # Cube_wall_list

Cube = m.GeometryObject(
    name = 'Cube',
    vertex_list = Cube_vertex_list,
    wall_list = Cube_wall_list,
    surface_regions = []
)
# ^^^^ Cube ^^^^


# ---- Transp ----
Transp_vertex_list = [
    [-0.446861803531647, -0.0345039367675781, -0.0282290726900101], 
    [-0.446861803531647, -0.0345039367675781, 0.471770942211151], 
    [-0.446861803531647, 0.465496063232422, -0.0282290726900101], 
    [-0.446861803531647, 0.465496063232422, 0.471770942211151], 
    [0.0531382113695145, -0.0345039367675781, -0.0282290726900101], 
    [0.0531382113695145, -0.0345039367675781, 0.471770942211151], 
    [0.0531382113695145, 0.465496063232422, -0.0282290726900101], 
    [0.0531382113695145, 0.465496063232422, 0.471770942211151]
] # Transp_vertex_list

Transp_wall_list = [
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
] # Transp_wall_list

Transp = m.GeometryObject(
    name = 'Transp',
    vertex_list = Transp_vertex_list,
    wall_list = Transp_wall_list,
    surface_regions = []
)
# ^^^^ Transp ^^^^


