# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

# ---- default_compartment ----
default_compartment_vertex_list = [
    [-0.0625, -0.0625, -0.0625], 
    [-0.0625, -0.0625, 0.0625], 
    [-0.0625, 0.0625, -0.0625], 
    [-0.0625, 0.0625, 0.0625], 
    [0.0625, -0.0625, -0.0625], 
    [0.0625, -0.0625, 0.0625], 
    [0.0625, 0.0625, -0.0625], 
    [0.0625, 0.0625, 0.0625]
] # default_compartment_vertex_list

default_compartment_wall_list = [
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
] # default_compartment_wall_list

default_compartment = m.GeometryObject(
    name = 'DEFAULT',
    vertex_list = default_compartment_vertex_list,
    wall_list = default_compartment_wall_list,
    surface_regions = []
)
# ^^^^ default_compartment ^^^^


# ---- EC ----
EC_vertex_list = [
    [-0.25, -0.25, -0.25], 
    [-0.25, -0.25, 0.25], 
    [-0.25, 0.25, -0.25], 
    [-0.25, 0.25, 0.25], 
    [0.25, -0.25, -0.25], 
    [0.25, -0.25, 0.25], 
    [0.25, 0.25, -0.25], 
    [0.25, 0.25, 0.25]
] # EC_vertex_list

EC_wall_list = [
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
] # EC_wall_list

EC = m.GeometryObject(
    name = 'EC',
    vertex_list = EC_vertex_list,
    wall_list = EC_wall_list,
    surface_regions = []
)
# ^^^^ EC ^^^^


# ---- CP ----
CP_vertex_list = [
    [-0.125, -0.125, -0.125], 
    [-0.125, -0.125, 0.125], 
    [-0.125, 0.125, -0.125], 
    [-0.125, 0.125, 0.125], 
    [0.125, -0.125, -0.125], 
    [0.125, -0.125, 0.125], 
    [0.125, 0.125, -0.125], 
    [0.125, 0.125, 0.125]
] # CP_vertex_list

CP_wall_list = [
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
] # CP_wall_list

CP = m.GeometryObject(
    name = 'CP',
    vertex_list = CP_vertex_list,
    wall_list = CP_wall_list,
    surface_regions = []
)
# ^^^^ CP ^^^^


