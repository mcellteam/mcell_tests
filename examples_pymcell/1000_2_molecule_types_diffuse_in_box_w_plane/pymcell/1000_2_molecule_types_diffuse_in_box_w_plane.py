#!/usr/bin/env python


# TODO: this is probably not the way how the inmport form a different directory should be done
import os
import sys
MCELL_DIR = os.environ.get('MCELL_DIR', '')

if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'python'))
else:
    print("Error: variable MCELL_DIR that allows to find mcell build directory was not set")
    
from pymcell import *

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
    world = MCellSim(seed=1)
    world.set_time_step(time_step=1e-6)
    iterations=1000
    world.set_iterations(iterations)

    # add geometry objects
    box_obj = MeshObj("Cube", box_vert_list, box_face_list, translation=(0, 0, 0))
    world.add_geometry(box_obj)
    
    plane_obj = MeshObj("Plane", plane_vert_list, plane_face_list, translation=(0, 0, 0))
    plane_reg = SurfaceRegion(plane_obj, 'reg', plane_reg_face_list)
    world.add_geometry(plane_obj)
        
    # Define volume molecules species
    species_a = Species("a", 1e-6)
    species_b = Species("b", 1e-6)
    world.add_species([species_a, species_b])
    
    # Their releases
    rel_diameter = Vector3(0.0, 0.0, 0.0)
    world.create_release_site(species_a, 10, "spherical", Vector3(0.0, 0.0, 0.1), rel_diameter)
    world.create_release_site(species_b, 10, "spherical", Vector3(0.0, 0.0, -0.1), rel_diameter)
    
    # Create viz data
    world.add_viz([species_a, species_b], True) # TODO: bin/ascii dump
    
    # this is nedcessary in order for the mcell_get_count function to work
    #world.add_count(species_a, box_obj) # note: changes the precision slightly for some reason... 
    
    # reg_swig_obj = self._regions[plane_obj.full_reg_name]
    # reg_sym = m.mcell_get_reg_sym(reg_swig_obj)
    #    create_count(world._world, )
    
    #species_sym = world._species[species_a.name]
    #mesh = world._mesh_objects[plane_obj.name]
    #mesh_sym = mcell_get_obj_sym(mesh)
    #count_str = "my_react_data/seed_%04d/%s_%s" % (
    #        world._seed, species_a.name, plane_obj.name)
    #count_list, os, out_times, output = create_count(
    #    world._world, mesh_sym, species_sym, count_str, 1e-5, REPORT_ALL_HITS)
    
    # TODO: dump state
    world.dump()
    
    world.set_output_freq(100)
    for i in range(iterations + 1):
        world.run_iteration()


    # COUNT_TRIG_STRUCT
    #a, b, c = mcell_get_counter_value(world._world, "Scene.Plane[reg]", 0)
    
    #print(a)
    #print(b)
    #print(c)

    #cnt = world.get_species_count(species_a, box_obj)
    #print("A : " + str(cnt))
        
        
    world.end_sim()
    
    
if __name__ == "__main__":
    main()
    
                