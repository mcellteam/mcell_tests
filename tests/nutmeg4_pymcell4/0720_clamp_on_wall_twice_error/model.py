#!/usr/bin/env python3

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

# only volume molecules: V is clamped on the inner side of two cubes
V = m.Species('V', diffusion_constant_3d = 1e-6)
clamp_sc = m.SurfaceClass(
    'clamp_sc', type = m.SurfacePropertyType.CONCENTRATION_CLAMP,
    affected_complex_pattern = m.Complex('V', orientation = m.Orientation.DOWN), concentration = 1e-6)
clamp_flux = m.SurfaceClass(
    'clamp_flux', type = m.SurfacePropertyType.FLUX_CLAMP,
    affected_complex_pattern = m.Complex('V', orientation = m.Orientation.DOWN), concentration = 1e-6)

def cube(name, x0, top_class):
    top = m.SurfaceRegion(name = 'top', wall_indices = [5, 11], surface_class = top_class)
    vertices = [[x + x0, y, z] for x, y, z in [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]]]
    return m.GeometryObject(
        name = name, vertex_list = vertices, wall_list = [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]],
        surface_regions = [top], surface_class = clamp_sc)

# box1: the class clamp_sc on ALL and on top, so the top walls get it twice;
# box2: clamp_sc on ALL and clamp_flux on top, two clamps of V on the same side
box1 = cube('box1', 0, clamp_sc)
box2 = cube('box2', 5, clamp_flux)

model = m.Model()
model.add_species(V)
model.add_surface_class(clamp_sc)
model.add_surface_class(clamp_flux)
model.add_geometry_object(box1)
model.add_geometry_object(box2)
model.config.time_step = 1e-6
model.config.total_iterations = 10
model.initialize()
model.run_iterations(10)
model.end_simulation()
