# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

# ---- up ----
up_vertex_list = [
    [-0.205813646316528, -0.236602157354355, 0.020], 
    [-0.205813646316528, -0.236602157354355, 0.100], 
    [-0.205813646316528, 0.163397818803787, 0.020], 
    [-0.205813646316528, 0.163397818803787, 0.100], 
    [0.194186329841614, -0.236602157354355, 0.020], 
    [0.194186329841614, -0.236602157354355, 0.100], 
    [0.194186329841614, 0.163397818803787, 0.020], 
    [0.194186329841614, 0.163397818803787, 0.100]
] # up_vertex_list

up_wall_list = [
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
] # up_wall_list

up = m.GeometryObject(
    name = 'up',
    vertex_list = up_vertex_list,
    wall_list = up_wall_list,
    surface_regions = []
)
# ^^^^ up ^^^^


# ---- bottom ----
bottom_vertex_list = [
    [-0.199999988079071, -0.199999988079071, -0.02], 
    [-0.199999988079071, -0.199999988079071, 0.018], # the gap is 2nm 
    [-0.199999988079071, 0.199999988079071, -0.02], 
    [-0.199999988079071, 0.199999988079071, 0.018], 
    [0.199999988079071, -0.199999988079071, -0.02], 
    [0.199999988079071, -0.199999988079071, 0.018], 
    [0.199999988079071, 0.199999988079071, -0.02], 
    [0.199999988079071, 0.199999988079071, 0.018]
] # bottom_vertex_list

bottom_wall_list = [
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
] # bottom_wall_list

bottom = m.GeometryObject(
    name = 'bottom',
    vertex_list = bottom_vertex_list,
    wall_list = bottom_wall_list,
    surface_regions = []
)
# ^^^^ bottom ^^^^


