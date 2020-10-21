import mcell as m

# ---- Tetrahedron ----
Tetrahedron_vertex_list = [
    [0, 0, 0.02], 
    [0.02, 0, -0.01], 
    [-0.01, 0.02, -0.01], 
    [-0.01, -0.02, -0.01]
] # Tetrahedron_vertex_list

Tetrahedron_element_connections = [
    [0, 1, 2], 
    [0, 2, 3], 
    [0, 3, 1], 
    [1, 3, 2]
] # Tetrahedron_element_connections

Tetrahedron = m.GeometryObject(
    name = 'Tetrahedron',
    vertex_list = Tetrahedron_vertex_list,
    element_connections = Tetrahedron_element_connections,
    surface_regions = []
)
# ^^^^ Tetrahedron ^^^^


