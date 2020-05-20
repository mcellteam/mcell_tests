import mcell as m

from parameters import *

# This generated file defines the following objects:
# box: m.GeometryObject

# ---- box ----
box_vertex_list = [
    [-0.05, -0.05, 0.05], 
    [-0.05, 0.05, -0.05], 
    [-0.05, -0.05, -0.05], 
    [-0.05, 0.05, 0.05], 
    [0.05, 0.05, -0.05], 
    [0.05, 0.05, 0.05], 
    [0.05, -0.05, -0.05], 
    [0.05, -0.05, 0.05]
] # box_vertex_list

box_element_connections = [
    [0, 1, 2], 
    [3, 4, 1], 
    [5, 6, 4], 
    [7, 2, 6], 
    [4, 2, 1], 
    [3, 7, 5], 
    [0, 3, 1], 
    [3, 5, 4], 
    [5, 7, 6], 
    [7, 0, 2], 
    [4, 6, 2], 
    [3, 0, 7]
] # box_element_connections

box = m.GeometryObject(
    name = 'box',
    vertex_list = box_vertex_list,
    element_connections = box_element_connections
)
# ^^^^ box ^^^^