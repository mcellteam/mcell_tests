#!/usr/bin/env python


# TODO: this is probably not the way how the inmport form a different directory should be done
import os
import sys
#import pandas as pd
#import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt

MCELL_DIR = os.environ.get('MCELL_DIR', '')

if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'python'))
else:
    print("Error: variable MCELL_DIR that allows to find mcell build directory was not set")

    
import pymcell as m

box_vert_list = [
    ( -0.25, -0.25, -0.25 ),
    ( -0.25, -0.25, 0.25 ),
    ( -0.25, 0.25, -0.25 ),
    ( -0.25, 0.25, 0.25 ),
    ( 0.25, -0.25, -0.25 ),
    ( 0.25, -0.25, 0.25 ),
    ( 0.25, 0.25, -0.25 ),
    ( 0.25, 0.25, 0.25 )
]
    
box_face_list = [
    ( 1, 2, 0 ),
    ( 3, 6, 2 ),
    ( 7, 4, 6 ),
    ( 5, 0, 4 ),
    ( 6, 0, 2 ),
    ( 3, 5, 7 ),
    ( 1, 3, 2 ),
    ( 3, 7, 6 ),
    ( 7, 5, 4 ),
    ( 5, 1, 0 ),
    ( 6, 4, 0 ),
    ( 3, 1, 5 )    
]    
    
    
plane_vert_list = [
    ( -0.25, -0.25, 0 ),
    ( 0.25, -0.25, 0 ),
    ( -0.25, 0.25, 0 ),
    ( 0.25, 0.25, 0 )
]

plane_face_list = [
    ( 1, 2, 0 ),
    ( 1, 3, 2 )
]    

plane_reg_face_list = [ 0, 1 ]

def main():
    world = m.mcell_create()
    m.mcell_init_state(world)
    dt = 1e-6
    iterations = 1000
    m.mcell_set_time_step(world, dt)
    m.mcell_set_iterations(world, iterations)
    m.mcell_set_seed(world, 1)

    # Create Scene for simulation
    scene_name = 'Scene'
    scene = m.create_instance_object(world, scene_name)
    
    # add geometry object with defined regions
    box_name = 'Cube'
    box_obj = m.create_polygon_object(world, box_vert_list, box_face_list, scene, box_name)

    plane_name = 'Plane'
    plane_obj = m.create_polygon_object(world, plane_vert_list, plane_face_list, scene, plane_name)
        
    reg_name = 'Raft1'
    reg = m.create_surface_region(world, plane_obj, plane_reg_face_list, reg_name) 
            
    # Define volume molecules species
    species_a = m.create_species(world, "a", 1e-6, False)
    species_b = m.create_species(world, "b", 1e-6, False)
    
    
    # Their releases 
    # Note: we are releasing molecules form a single point, this means that for several initial iterations, 
    # there will be less hits, it would be better to do release the molecules uniformly in the top and bottom half-cubes
    rel_location_a = m.Vector3(0.0, 0.0, 0.1)
    rel_location_b = m.Vector3(0.0, 0.0, -0.1)
    rel_diameter = m.Vector3(0.0, 0.0, 0.0)
    
    position_a, diameter_a, sphere_release_object_a = m.create_release_site(
        world, scene, rel_location_a, rel_diameter, m.SHAPE_SPHERICAL, 500, 0, species_a,
        "rel_a")

    position_b, diameter_b, sphere_release_object_b = m.create_release_site(
        world, scene, rel_location_b, rel_diameter, m.SHAPE_SPHERICAL, 500, 0, species_b,
        "rel_n")

    # Create viz data
    viz_list = m.mcell_add_to_species_list(species_a, False, 0, None)
    viz_list = m.mcell_add_to_species_list(species_b, False, 0, viz_list)
    
    m.mcell_create_viz_output(
        world, "./viz_data/seed_0001/Scene", viz_list, 0, iterations, 1, True)
        
    m.mcell_init_simulation(world)
    m.mcell_init_output(world)
    
    # Run for several interations
    output_freq = 100
    for i in range(iterations + 1):
        m.mcell_run_iteration(world, output_freq, 0)

    m.mcell_flush_data(world)
    m.mcell_print_final_warnings(world)
    m.mcell_print_final_statistics(world)
        
    
if __name__ == "__main__":
    main()
    
                