# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

# ---- Cube ----
Cube_vertex_list = [
    [-0.05, -0.05, -0.05], 
    [-0.05, -0.05, 0.05], 
    [-0.05, 0.05, -0.05], 
    [-0.05, 0.05, 0.05], 
    [0.05, -0.05, -0.05], 
    [0.05, -0.05, 0.05], 
    [0.05, 0.05, -0.05], 
    [0.05, 0.05, 0.05]
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

Cube_membrane_wall_indices = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
] #Cube_membrane_wall_indices

Cube_membrane = m.SurfaceRegion(
    name = 'membrane',
    wall_indices = Cube_membrane_wall_indices
)

Cube = m.GeometryObject(
    name = 'Cube',
    vertex_list = Cube_vertex_list,
    wall_list = Cube_wall_list,
    surface_regions = [Cube_membrane]
)
# ^^^^ Cube ^^^^


