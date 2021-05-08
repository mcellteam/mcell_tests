import mcell as m

color_default = m.Color(1, 1, 1, 0.25)
color_red = m.Color(1, 0, 0, 0.25)
color_green = m.Color(0, 1, 0, 0.25)

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

Cube_left_side_wall_indices = [
    3, 9
] #Cube_left_side_wall_indices

Cube_left_side = m.SurfaceRegion(
    name = 'left_side',
    wall_indices = Cube_left_side_wall_indices,
    initial_color = color_green
)

Cube_right_side_wall_indices = [
    1, 7
] #Cube_right_side_wall_indices

Cube_right_side = m.SurfaceRegion(
    name = 'right_side',
    wall_indices = Cube_right_side_wall_indices,
    initial_color = color_red
)

Cube = m.GeometryObject(
    name = 'Cube',
    vertex_list = Cube_vertex_list,
    wall_list = Cube_wall_list,
    surface_regions = [Cube_left_side, Cube_right_side],
    initial_color = color_default
)
# ^^^^ Cube ^^^^


