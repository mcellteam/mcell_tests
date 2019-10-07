#!/usr/bin/env python


# TODO: this is probably not the way how the inmport form a different directory should be done
import os
import sys
import pandas as pd
import numpy as np

import icosphere

MCELL_DIR = os.environ.get('MCELL_DIR', '')

if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'python'))
else:
    print("Error: variable MCELL_DIR that allows to find mcell build directory was not set")
    
import pymcell as m


def main():
    world = m.mcell_create()
    m.mcell_init_state(world)

    dt = 1e-5
    iterations = 1000
    m.mcell_set_time_step(world, dt)
    m.mcell_set_iterations(world, iterations)

    # Create Scene for simulation
    scene_name = 'Scene'
    scene = m.create_instance_object(world, scene_name)

    # add geometry object with defined regions
    ico_name = 'Icosphere'
    ico_mesh = m.create_polygon_object(world, icosphere.vert_list, icosphere.face_list, scene, ico_name)

    raft1_name = 'Raft1'
    raft1_reg = m.create_surface_region(world, ico_mesh, icosphere.raft1_surface_face_list, raft1_name) 

    raft2_name = 'Raft2'
    raft2_reg = m.create_surface_region(world, ico_mesh, icosphere.raft2_surface_face_list, raft2_name) 

    # Define surface molecules species
    species_rf_sym = m.create_species(world, "Rf", 1e-6, True)
    species_rs_sym = m.create_species(world, "Rs", 1e-9, True)
    species_chol_sym = m.create_species(world, "chol", 1e-6, True)
    
    
    #all_species = [species_rf_sym, species_rs_sym, species_chol_sym]
    #world.add_species(all_species)

    # Create viz data
    # 1 - up, -1 - down, 0 - no orientation
    viz_list = m.mcell_add_to_species_list(species_rf_sym, True, 1, None)
    viz_list = m.mcell_add_to_species_list(species_rs_sym, True, 1, viz_list)
    viz_list = m.mcell_add_to_species_list(species_chol_sym, True, 1, viz_list)
    
    m.mcell_create_viz_output(
        world, "./viz_data/seed_0001/Scene", viz_list, 0, iterations, 1, True)

    sc_name = 'reflect_chol'
    sc_sym = m.create_surf_class(world, sc_name)
    
    m.mcell_add_surf_class_properties(
                world, m.RFLCT, sc_sym, species_chol_sym, 0)

    m.mcell_assign_surf_class_to_region(sc_sym, raft1_reg)
    m.mcell_assign_surf_class_to_region(sc_sym, raft2_reg)

    # Their releases
    # orientation? - should be ' (up)
    release_chol_raft1 = m.create_region_release_site(
        world, scene, ico_mesh, 'raft1_rel', raft1_name, 250, 0, species_chol_sym, True, 1)  # 0 - constant number to release
    release_chol_raft2 = m.create_region_release_site(
        world, scene, ico_mesh, 'raft2_rel', raft2_name, 100, 0, species_chol_sym, True, 1)
    release_rf = m.create_region_release_site(
        world, scene, ico_mesh, 'ico_rel', 'ALL', 1000, 0, species_rf_sym, True, 1)    
    

    # define reactions
    reactants = m.mcell_add_to_species_list(species_rf_sym, True, 1, None)
    reactants = m.mcell_add_to_species_list(species_chol_sym, True, 1, reactants)
    
    products = m.mcell_add_to_species_list(species_rs_sym, True, 1, None)
    products = m.mcell_add_to_species_list(species_chol_sym, True, 1, products)

    m.create_reaction(world, reactants, products, 1e8, name="rxn")


    # Initialize simulation
    # m.mcell_update_root_instance(world) # FIXME: insert into init sim
    m.mcell_init_simulation(world)
    m.mcell_init_output(world)
    
    m.mcell_dump_state(world)


        
    # Run for several interations
    output_freq = 100
    for i in range(iterations + 1):
        m.mcell_run_iteration(world, output_freq, 0)
        
    m.mcell_flush_data(world)
    
    
if __name__ == "__main__":
    main()
    
                