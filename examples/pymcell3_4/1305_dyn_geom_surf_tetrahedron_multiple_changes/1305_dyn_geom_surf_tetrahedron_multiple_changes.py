#!/usr/bin/env python3

import os
import sys

MCELL_DIR = os.environ.get('MCELL_DIR', '')

if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'python'))
else:
    print("Error: variable MCELL_DIR that allows to find mcell build directory was not set")

    
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
    

def main():
    world = m.mcell_create()
    m.mcell_init_state(world)
    dt = 1e-6
    iterations = 50
    m.mcell_set_time_step(world, dt)
    m.mcell_set_iterations(world, iterations)
    m.mcell_set_seed(world, 1)
    m.mcell_set_with_checks_flag(world, 0)
    m.mcell_set_randomize_smol_pos(world, 0)
    
    # Create Scene for simulation
    scene_name = 'Scene'
    scene = m.create_instance_object(world, scene_name)
    
    # add geometry object with defined regions
    box_name = 'Tetrahedron'
    box_obj = m.create_polygon_object(world, tetrahedron_vert_list, tetrahedron_face_list, scene, box_name)

    # Define volume molecules species
    species_a = m.create_species(world, "sm", 1e-7, True)
    
   
    # Their releases 
    release_a = m.create_region_release_site(
        world, scene, box_obj, 'Tetrahedron_rel', 'ALL', 10, 0, species_a, True, 1)  # 0 - constant number to release

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
    p = world4.get_partition(0)
    
    output_freq = 100
    lu = world4.config.length_unit;
    
    for i in range(iterations + 1):
        
        # mcell3 does geometry change as the first thing in an iteration 
        if i == 10:
            # even with this small change, some molecules are placed to a different wall than 
            # what moved it in mcell3
            displacement = m.Vec3(0, 0, -0.01/lu) 
            p.add_vertex_move(0, displacement)
            p.apply_vertex_moves()
            
        if i == 20:
            displacement = m.Vec3(0.01/lu, 0.01/lu, 0.01/lu) 
            p.add_vertex_move(0, displacement)
            p.apply_vertex_moves()

        if i == 30:
            displacement0 = m.Vec3(0, 0, -0.01/lu) 
            p.add_vertex_move(0, displacement0)
            displacement1 = m.Vec3(-0.01/lu, 0, 0) 
            p.add_vertex_move(1, displacement1)
            displacement2 = m.Vec3(0, -0.01/lu, 0) 
            p.add_vertex_move(2, displacement2)
            displacement3 = m.Vec3(0, +0.01/lu, 0) 
            p.add_vertex_move(3, displacement3)
            p.apply_vertex_moves()

        if i == 40:
            displacement0 = m.Vec3(0, 0, +0.01/lu) 
            p.add_vertex_move(0, displacement0)
            displacement1 = m.Vec3(-0.005/lu, 0, 0) 
            p.add_vertex_move(1, displacement1)
            #displacement2 = m.Vec3(0, -0.01/lu, 0) 
            #p.add_vertex_move(2, displacement2)
            displacement3 = m.Vec3(0, 0, -0.01/lu) 
            p.add_vertex_move(3, displacement3)
            p.apply_vertex_moves()
            
        print("Iteration " + str(i) + " started")
        sys.stdout.flush()

        world4.run_n_iterations(1, output_freq)
            
            
    world4.end_simulation()
        
    
if __name__ == "__main__":
    main()
    
                