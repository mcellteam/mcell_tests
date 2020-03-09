#!/usr/bin/env python


# TODO: this is probably not the way how the import form a different directory should be done
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
    
# all faces
tetrahedron_surface_face_list = [
    0, 1, 2, 3
]    

def main():
    
    world = m.mcell_create()
    m.mcell_init_state(world)
    dt = 1e-6
    iterations = 20
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

    #reg_name = 'Tetrahedron_reg'
    #reg = m.create_surface_region(world, box_obj, tetrahedron_surface_face_list, reg_name) 


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
    
    #m.mcell_dump_state(world)
    #sys.exit(0)
    
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
    for i in range(iterations + 1):
        
        # mcell3 does geometry change as the first thing in an iteration
        if i == 10:
            # change geometry of vertex 0
            # the recomputation of units should be done preferably by the API
            #  but for now we do it here
            displacement = m.Vec3(0, 0, 0.01/world4.config.length_unit) 
            p.add_vertex_move(0, displacement)

            # update molecules after geonetry has changed
            p.apply_vertex_moves()
            
            #world4.dump()
            
        print("Iteration " + str(i) + " started")
        sys.stdout.flush()

        world4.run_n_iterations(1, output_freq)
            
            
    world4.end_simulation()
        
    
if __name__ == "__main__":
    main()
    
                