import mcell as m

# ---- CP ----
CP_vertex_list = [
    [-0.25, -0.25, -0.25], 
    [-0.25, -0.25, 0.25], 
    [-0.25, 0.25, -0.25], 
    [-0.25, 0.25, 0.25], 
    [0.25, -0.25, -0.25], 
    [0.25, -0.25, 0.25], 
    [0.25, 0.25, -0.25], 
    [0.25, 0.25, 0.25]
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


# ---- EC ----
EC_vertex_list = [
    [-0.5, -0.5, -0.5], 
    [-0.5, -0.5, 0.5], 
    [-0.5, 0.5, -0.5], 
    [-0.5, 0.5, 0.5], 
    [0.5, -0.5, -0.5], 
    [0.5, -0.5, 0.5], 
    [0.5, 0.5, -0.5], 
    [0.5, 0.5, 0.5]
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


