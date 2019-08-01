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
    
def create_box(world):
    box_obj = MeshObj("Cube", box_vert_list, box_face_list, translation=(0, 0, 0))
    world.add_geometry(box_obj)


def create_plane(world):
    # FIXME: when the name is "Cube", pymcell segfaults
    plane_obj = MeshObj("Plane", plane_vert_list, plane_face_list, translation=(0, 0, 0))
    world.add_geometry(plane_obj)
     

def main():
    world = MCellSim(seed=1)
    world.set_time_step(time_step=1e-6)
    iterations=1000
    world.set_iterations(iterations)

    # add geometry objects
    create_box(world)
    create_plane(world)
        
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
    
    world.set_output_freq(100)
    for i in range(iterations + 1):
        world.run_iteration()
        
    world.end_sim()
    
    
if __name__ == "__main__":
    main()
    
                