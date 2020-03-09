#!/usr/bin/env python3

# corresponds to 3020_base_dyn_geom_cube_multiple_changes

# TODO: this is probably not the way how the import form a different directory should be done
import os
import sys

MCELL_DIR = os.environ.get('MCELL_DIR', '')

if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'python'))
else:
    print("Error: variable MCELL_DIR that allows to find mcell build directory was not set")

    
import pymcell as m

    
cube_vert_list = [
    [  0.01,  0.01, -0.01 ], # 0
    [  0.01, -0.01, -0.01 ], # 1
    [ -0.01, -0.01, -0.01 ], # 2
    [ -0.01,  0.01, -0.01 ], # 3
    [  0.01,  0.01,  0.01 ], # 4
    [  0.01, -0.01,  0.01 ], # 5
    [ -0.01, -0.01,  0.01 ], # 6
    [ -0.01,  0.01,  0.01 ]  # 7
]

cube_face_list = [
    [ 0, 1, 2 ],
    [ 4, 7, 5 ], # 1
    [ 0, 4, 1 ],
    [ 1, 5, 2 ],
    [ 2, 6, 7 ],
    [ 4, 0, 7 ], # 5
    [ 3, 0, 2 ],
    [ 4, 5, 1 ],
    [ 0, 3, 7 ],
    [ 7, 6, 5 ],
    [ 3, 2, 7 ],
    [ 5, 6, 2 ]
]    


def main():
    
    world = m.mcell_create()
    m.mcell_init_state(world)
    dt = 1e-6
    iterations = 60
    m.mcell_set_time_step(world, dt)
    m.mcell_set_iterations(world, iterations)
    m.mcell_set_seed(world, 1)

    # Create Scene for simulation
    scene_name = 'Scene'
    scene = m.create_instance_object(world, scene_name)
    
    # add geometry object with defined regions
    box_name = 'Cube'
    box_obj = m.create_polygon_object(world, cube_vert_list, cube_face_list, scene, box_name)

    # Define volume molecules species
    species_a = m.create_species(world, "vm", 1e-5, False)
    
    
    # Their releases 
    # Note: we are releasing molecules form a single point, this means that for several initial iterations, 
    # there will be less hits, it would be better to do release the molecules uniformly in the top and bottom half-cubes
    rel_location_a = m.Vector3(0.0, 0.0, 0.0)
    rel_diameter = m.Vector3(0.02, 0.02, 0.02)
    
    position_a, diameter_a, sphere_release_object_a = m.create_release_site(
        world, scene, rel_location_a, rel_diameter, m.SHAPE_SPHERICAL, 100, 0, species_a,
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
    
    #p.dump();
    
    output_freq = 10
    lu = world4.config.length_unit;
    
    for i in range(iterations + 1):
        
        if i == 20:
            displacement0 = m.Vec3(0.01/lu, 0.01/lu, -0.01/lu) 
            p.add_vertex_move(0, displacement0)
            displacement4 = m.Vec3(0.01/lu, 0.01/lu, 0.01/lu) 
            p.add_vertex_move(4, displacement4)
            p.apply_vertex_moves()
            
            #p.dump();

        if i == 40:
            displacement0 = m.Vec3(-0.01/lu, -0.01/lu, +0.01/lu) 
            p.add_vertex_move(0, displacement0)
            displacement4 = m.Vec3(-0.01/lu, -0.01/lu, -0.01/lu) 
            p.add_vertex_move(4, displacement4)
            p.apply_vertex_moves()
            
            p.dump();
            
        #print("Iteration " + str(i) + " started")
        sys.stdout.flush()

        world4.run_n_iterations(1, output_freq)
            
            
    world4.end_simulation()
        
    
if __name__ == "__main__":
    main()
    
                