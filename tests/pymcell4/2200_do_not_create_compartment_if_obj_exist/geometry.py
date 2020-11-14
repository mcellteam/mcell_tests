import mcell as m

# ---- Compartment ----
Compartment_vertex_list = [
    [0, 0, 0.02], 
    [0.02, 0, -0.01], 
    [-0.01, 0.02, -0.01], 
    [-0.01, -0.02, -0.01]
] # Compartment_vertex_list

Compartment_wall_list = [
    [0, 1, 2], 
    [0, 2, 3], 
    [0, 3, 1], 
    [1, 3, 2]
] # Compartment_wall_list

Compartment = m.GeometryObject(
    name = 'Compartment',
    vertex_list = Compartment_vertex_list,
    wall_list = Compartment_wall_list,
    surface_regions = []
)
# ^^^^ Compartment ^^^^


