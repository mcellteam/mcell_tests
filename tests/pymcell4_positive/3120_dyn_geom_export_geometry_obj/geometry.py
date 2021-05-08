import mcell as m

# ---- Tetrahedron ----
Tetrahedron_vertex_list = [
    [0, 0, 0.02], 
    [0.02, 0, -0.01], 
    [-0.01, 0.02, -0.01], 
    [-0.01, -0.02, -0.01]
] # Tetrahedron_vertex_list

Tetrahedron_wall_list = [
    [0, 1, 2], 
    [0, 2, 3], 
    [0, 3, 1], 
    [1, 3, 2]
] # Tetrahedron_wall_list

Tetrahedron = m.GeometryObject(
    name = 'Tetrahedron',
    vertex_list = Tetrahedron_vertex_list,
    wall_list = Tetrahedron_wall_list,
    surface_regions = []
)
# ^^^^ Tetrahedron ^^^^


