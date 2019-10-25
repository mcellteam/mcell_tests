#!/usr/bin/env python

# same as example 0000 but using object-oriented API
# not checking any reference data

# TODO: this is probably not the way how the inport form a different directory should be done
import os
import sys
MCELL_DIR = os.environ.get('MCELL_DIR', '')

if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'python'))
else:
    print("Error: variable MCELL_DIR that allows to find mcell build directory was not set")
    
from pymcell import *



def main():
    
    world = MCellSim(seed=1)
    world.set_time_step(time_step=1e-6)
    iterations=1000
    world.set_iterations(iterations)
    
    # Define volume molecules species
    species_a = Species("a", 1e-6)
    world.add_species(species_a)
    
    rel_location = Vector3(0.0, 0.0, 0.0)
    rel_diameter = Vector3(0.0, 0.0, 0.0)
   
    world.create_release_site(species_a, 2, "spherical", rel_location, rel_diameter)

    # Create viz data - add ad ASCII
    world.add_viz([species_a])

    world.set_output_freq(100)
    for i in range(iterations + 1):
        world.run_iteration()
        
    world.end_sim()
    
    
if __name__ == "__main__":
    main()
    
                