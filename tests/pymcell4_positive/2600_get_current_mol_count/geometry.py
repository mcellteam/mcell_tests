import mcell as m

# ---- Cube1 ----
Cube1_vertex_list = [
    [-0.1, -0.1, -0.1], 
    [-0.1, -0.1, 0.1], 
    [-0.1, 0.1, -0.1], 
    [-0.1, 0.1, 0.1], 
    [0.1, -0.1, -0.1], 
    [0.1, -0.1, 0.1], 
    [0.1, 0.1, -0.1], 
    [0.1, 0.1, 0.1]
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
    [-0.2, -0.2, -0.2], 
    [-0.2, -0.2, 0.2], 
    [-0.2, 0.2, -0.2], 
    [-0.2, 0.2, 0.2], 
    [0.2, -0.2, -0.2], 
    [0.2, -0.2, 0.2], 
    [0.2, 0.2, -0.2], 
    [0.2, 0.2, 0.2]
] # Cube2_vertex_list

Cube2_wall_list = [
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
] # Cube2_wall_list

Cube2 = m.GeometryObject(
    name = 'Cube2',
    vertex_list = Cube2_vertex_list,
    wall_list = Cube2_wall_list,
    surface_regions = []
)
# ^^^^ Cube2 ^^^^


# ---- Cube3 ----
Cube3_vertex_list = [
    [-0.3, -0.3, -0.3], 
    [-0.3, -0.3, 0.3], 
    [-0.3, 0.3, -0.3], 
    [-0.3, 0.3, 0.3], 
    [0.3, -0.3, -0.3], 
    [0.3, -0.3, 0.3], 
    [0.3, 0.3, -0.3], 
    [0.3, 0.3, 0.3]
] # Cube3_vertex_list

Cube3_wall_list = [
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
] # Cube3_wall_list

Cube3 = m.GeometryObject(
    name = 'Cube3',
    vertex_list = Cube3_vertex_list,
    wall_list = Cube3_wall_list,
    surface_regions = []
)
# ^^^^ Cube3 ^^^^


