#!/usr/bin/env python


# TODO: this is probably not the way how the inmport form a different directory should be done
import os
import sys
import pandas as pd
import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt

MCELL_PATH = os.environ.get('MCELL_PATH', '')

if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'python'))
else:
    print("Error: variable MCELL_PATH that allows to find mcell build directory was not set")
    
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
 that holds the information and is dumped when the busser size reaches a threshold.
 Using these data right now would mean risking losing some of the hits. 
 This is something that will be improved in the close future, but for now
 a simple solution where we instruct mcell to dump every single item and 
 read the whole file was chosen. 
  
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
    # Note: we are releasing molecules form a single point, this means that for several initial iterations, 
    # there will be less hits, it would be better to do release the molecules uniformly in the top and bottom half-cubes
    rel_diameter = Vector3(0.0, 0.0, 0.0)
    world.create_release_site(species_a, 500, "spherical", Vector3(0.0, 0.0, 0.1), rel_diameter)
    world.create_release_site(species_b, 500, "spherical", Vector3(0.0, 0.0, -0.1), rel_diameter)
    
    # Create viz data
    world.add_viz([species_a, species_b], ascii_output=True)
    
    # Create counter for hits of the plane
    # TODO: make this API nicer     
    species_sym_a = world._species[species_a.name]
    mesh = world._mesh_objects[plane_obj.name]
    
    mesh_sym = mcell_get_obj_sym(mesh)
    count_str_a = "react_data/seed_%04d/%s.%s.hits.dat" % (
            world._seed, species_a.name, plane_obj.name)
    count_list_a, os_a, out_times_a, output_a = create_count(
        world._world, mesh_sym, species_sym_a, count_str_a, step=1e-5, 
        report_flags=(REPORT_ALL_HITS | REPORT_TRIGGER), exact_time=1, buffer_size=1)
    world._counts[count_str_a] = (count_list_a, os_a, out_times_a, output_a)

    species_sym_b = world._species[species_b.name]
    count_str_b = "react_data/seed_%04d/%s.%s.hits.dat" % (
            world._seed, species_b.name, plane_obj.name)
    count_list_b, os_b, out_times_b, output_b = create_count(
        world._world, mesh_sym, species_sym_b, count_str_b, step=1e-5, 
        report_flags=(REPORT_ALL_HITS | REPORT_TRIGGER), exact_time=1, buffer_size=1)
    world._counts[count_str_b] = (count_list_b, os_b, out_times_b, output_b)

    # Dump internal mcell state
    #world.dump()
    
    # Run for several interations
    hits_a = []
    hits_b = []
    output_freq = 100
    world.set_output_freq(output_freq)
    for i in range(iterations + 1):
        world.run_iteration()
        
        # for now, we are loading all data each iteration...
        # this will be optimized later 
        df_a = load_hits_data(count_str_a)
        df_a = df_a[ np.abs(df_a['iter'] - i/1e6) < 1e-8 ]
        hits_a.append(len(df_a))
        
        #if not df_a.empty:
        #    print("Hits from top in iteration " + str(i))
        #    print(df_a)

        df_b = load_hits_data(count_str_b)
        df_b = df_b[ np.abs(df_b['iter'] - i/1e6) < 1e-8 ]
        hits_b.append(len(df_b))
        
        
    # print differences in hits for each iterations
    for i in range(0, len(hits_a)):
        print(str(i) + ": " + str(hits_a[i] - hits_b[i]))
    
    
    # Show histogram:
    #num_bins = 50
    #n, bins, patches = plt.hist(hits_a, num_bins, facecolor='blue', alpha=0.5)
    #plt.show()
    
    world.end_sim()
    
    
if __name__ == "__main__":
    main()
    
                