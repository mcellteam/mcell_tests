# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

# ---- box ----
box_vertex_list = [
    [-0.234999999403954, -0.234999999403954, -2.5], 
    [-0.234999999403954, -0.234999999403954, 2.5], 
    [-0.234999999403954, 0.234999999403954, -2.5], 
    [-0.234999999403954, 0.234999999403954, 2.5], 
    [0.234999999403954, -0.234999999403954, -2.5], 
    [0.234999999403954, -0.234999999403954, 2.5], 
    [0.234999999403954, 0.234999999403954, -2.5], 
    [0.234999999403954, 0.234999999403954, 2.5]
] # box_vertex_list

box_wall_list = [
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
] # box_wall_list

box_bottom_wall_indices = [
    4, 10
] #box_bottom_wall_indices

box_bottom = m.SurfaceRegion(
    name = 'bottom',
    wall_indices = box_bottom_wall_indices
)

box = m.GeometryObject(
    name = 'box',
    vertex_list = box_vertex_list,
    wall_list = box_wall_list,
    surface_regions = [box_bottom]
)
# ^^^^ box ^^^^


