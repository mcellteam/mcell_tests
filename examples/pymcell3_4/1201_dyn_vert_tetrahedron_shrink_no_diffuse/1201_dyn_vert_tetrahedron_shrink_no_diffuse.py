#!/usr/bin/env python3


# TODO: this is probably not the way how the inmport form a different directory should be done
import os
import sys
#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

MCELL_PATH = os.environ.get('MCELL_PATH', '')

if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'python'))
else:
    print("Error: variable MCELL_PATH that allows to find mcell build directory was not set")

    
import pymcell as m

    
tetrahedron_vert_list = [
    [  0.00,  0.00,  0.02 ],
    [  0.02,  0.00, -0.01 ],
    [ -0.01,  0.02, -0.01 ],
    [ -0.01, -0.02, -0.01 ]
]

tetrahedron_face_list = [
    [ 0, 1, 2 ],
    [ 0, 2, 3 ],
    [ 0, 3, 1 ],
    [ 1, 3, 2 ]
]    
    
def display_terahedron():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    tetrahedron_vert_array = np.array(tetrahedron_vert_list)
    
    print(str(tetrahedron_vert_array[:,0]))
    
    # points
    ax.scatter(tetrahedron_vert_array[:,0], tetrahedron_vert_array[:,1], tetrahedron_vert_array[:,2], c='r', marker='o')
    
    # lines?
    
    plt.show()


def main():
    # display 
    if len(sys.argv) == 2 and sys.argv[1] == 'show':
        display_terahedron()
        sys.exit(0) 
    
    
    
    world = m.mcell_create()
    m.mcell_init_state(world)
    dt = 1e-6
    iterations = 2
    m.mcell_set_time_step(world, dt)
    m.mcell_set_iterations(world, iterations)
    m.mcell_set_seed(world, 1)

    # Create Scene for simulation
    scene_name = 'Scene'
    scene = m.create_instance_object(world, scene_name)
    
    # add geometry object with defined regions
    box_name = 'Tetrahedron'
    box_obj = m.create_polygon_object(world, tetrahedron_vert_list, tetrahedron_face_list, scene, box_name)

    # Define volume molecules species
    species_a = m.create_species(world, "vm", 0, False)
    
    
    # Their releases 
    # Note: we are releasing molecules form a single point, this means that for several initial iterations, 
    # there will be less hits, it would be better to do release the molecules uniformly in the top and bottom half-cubes
    rel_location_a = m.Vector3(0.0, 0.0, 0.0)
    rel_diameter = m.Vector3(0.02, 0.02, 0.02)
    
    position_a, diameter_a, sphere_release_object_a = m.create_release_site(
        world, scene, rel_location_a, rel_diameter, m.SHAPE_SPHERICAL, 4, 0, species_a,
        "rel_a")

    # Create viz data
    viz_list = m.mcell_add_to_species_list(species_a, False, 0, None)
    
    m.mcell_create_viz_output(
        world, "./viz_data/seed_0001/Scene", viz_list, 0, iterations, 1, True)
        
    m.mcell_init_simulation(world)
    m.mcell_init_output(world)
    
    # until now we used just mcell3 interface
    # what follows is mcell4 C++ interface (without any wrappers)
    converter = m.MCell3WorldConverter()
    
    ok = converter.convert(world)
    if not ok:
        print("Conversion failed")
        sys.exit(1)
        
    world4 = converter.world
    
    # print vertices
    p = world4.get_partition(0)
    #cnt = p.get_geometry_vertex_count()
    #for i in range(cnt):
    #    vert = p.get_geometry_vertex(i)
    #    print("V" + str(i) + ": " + str(vert.x) + ", " + str(vert.y)+ ", " + str(vert.z))
    
    output_freq = 100
    for i in range(iterations + 1):
        
        # mcell3 does geometry change as the first thing in an iteration 
        if i == 2:
            # change geometry of vertex 0
            # the recomputation of units should be done preferably by the API
            #  but for now we do it here
            displacement = m.Vec3(0, 0, -0.01/world4.config.length_unit) 
            p.add_vertex_move(0, displacement)

            # update molecules after geonetry has changed
            p.apply_vertex_moves()
            
            world4.dump()
            
            
        print("Iteration " + str(i) + " started")
        sys.stdout.flush()

        world4.run_n_iterations(1, output_freq)
            
            
    world4.end_simulation()
        
    
if __name__ == "__main__":
    main()
    
                