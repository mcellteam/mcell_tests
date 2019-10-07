#!/usr/bin/env python


# TODO: this is probably not the way how the inport form a different directory should be done
import os
import sys
MCELL_DIR = os.environ.get('MCELL_DIR', '')

if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'python'))
else:
    print("Error: variable MCELL_DIR that allows to find mcell build directory was not set")
    
import pymcell as m



def main():
    world = m.mcell_create()
    m.mcell_init_state(world)
    
    iterations = 1000
    time_step = 1e-6
    
    m.mcell_set_time_step(world, time_step)
    m.mcell_set_iterations(world, iterations)
    
    # Define volume molecules species
    species_a = m.create_species(world, "a", 1e-6, False)
    
    # This is the world object. We just call it "Scene" here to be consistent
    # with the MDL output from Blender.
    scene_name = "Scene"
    scene = m.create_instance_object(world, scene_name)
    
    rel_location = m.Vector3(0.0, 0.0, 0.0)
    rel_diameter = m.Vector3(0.0, 0.0, 0.0)

    # we need to refine a release site for our molecules
    # FIXME: for some reason, not copying the resulting objects (unused) causes
    # the release information to be ignored     
    position, diameter, sphere_release_object = m.create_release_site(
        world, scene, rel_location, rel_diameter, m.SHAPE_SPHERICAL, 2, 0, species_a,
        "rel_a")
    
    # Create viz data
    viz_list = m.mcell_add_to_species_list(species_a, False, 0, None)
    m.mcell_create_viz_output(world, "./viz_data/pymcell/Scene", viz_list, 0, iterations, 1, True)

    
    m.mcell_init_simulation(world)
    m.mcell_init_output(world)
    
    output_freq = 100
    for i in range(iterations + 1):
        m.mcell_run_iteration(world, output_freq, 0)
        
    m.mcell_flush_data(world)
    m.mcell_print_final_warnings(world)
    m.mcell_print_final_statistics(world)
    
    
if __name__ == "__main__":
    main()
    
                