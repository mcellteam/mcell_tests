#!/usr/bin/env python


# TODO: this is probably not the way how the inmport form a different directory should be done
import os
import sys
import pandas as pd
import numpy as np

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

"""
 The current implementation in MCell has a fixed size of a buffer
 that holds the information and is dumped when .
 This is something that will be improved in the close future, but for now 
  
 A variant where we would extend the size of the buffer is also possible 
 and can be implemented. I hoped that for the initial steps, 
 some variant, although not very fast, could be sufficient.  
""" 
def load_hits_data(fname):
    data = []
    
    df = pd.read_csv(fname, delimiter=' ', header=None, index_col=False,
                         names=['iter', 'time', 'x_hit', 'y_hit', 'z_hit', 'orient'])
    return df


def main():
    world = MCellSim(seed=1)
    world.set_time_step(time_step=1e-6)
    iterations=1000 # 1000
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
    world.add_viz([species_a, species_b], ascii_output=True)
    
    # Create counter for hits of the plane
    # TODO: make this API nicer     
    species_sym = world._species[species_a.name]
    mesh = world._mesh_objects[plane_obj.name]
    
    mesh_sym = mcell_get_obj_sym(mesh)
    count_str = "react_data/seed_%04d/%s.%s.hits.dat" % (
            world._seed, species_a.name, plane_obj.name)
    count_list, os, out_times, output = create_count(
        world._world, mesh_sym, species_sym, count_str, step=1e-5, 
        report_flags=(REPORT_ALL_HITS | REPORT_TRIGGER), exact_time=1, buffer_size=1)
    world._counts[count_str] = (count_list, os, out_times, output)

    # Dump internal mcell state
    #world.dump()
    
    # Run for several interations
    output_freq = 100
    world.set_output_freq(output_freq)
    for i in range(iterations + 1):
        world.run_iteration()
        
        # for now, we are loading all data each iteration...
        # but this will be optimized little later 
        df = load_hits_data(count_str)
        df = df[ np.abs(df['iter'] - i/1e6) < 1e-8 ]
        if not df.empty:
            print("Hit in iteration " + str(i))
            print(df)
        
    #world.dump()
        
    world.end_sim()
    
    
if __name__ == "__main__":
    main()
    
                