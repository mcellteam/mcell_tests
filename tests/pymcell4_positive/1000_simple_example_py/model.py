#!/usr/bin/env python3

# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import sys
import os
import importlib.util

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

# ---- import mcell module located in directory ----
# ---- specified by system variable MCELL_PATH  ----
MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    if os.path.exists(os.path.join(lib_path, 'mcell.so')) or \
        os.path.exists(os.path.join(lib_path, 'mcell.pyd')):
        sys.path.append(lib_path)
    else:
        print("Error: Python module mcell.so or mcell.pyd was not found in "
              "directory '" + lib_path + "' constructed from system variable "
              "MCELL_PATH.")
        sys.exit(1)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)



import mcell as m

subsystem = m.Subsystem()
a = m.Species(
    name = 'a',                        # this species will be called 'a'  
    diffusion_constant_3d = 1e-6       # 'a' is a volume molecule (diffuses in 3d space)
)
subsystem.add_species(a)

instantiation = m.Instantiation()
rel_a = m.ReleaseSite(         # ReleaseSite defines molecule releases
    name = 'rel_a',
    complex = a,
    number_to_release = 10,            # 10  
    location = (0, 0, 0)               # all molecules will be released at origin 
)
instantiation.add_release_site(rel_a)  

model = m.Model()
model.add_subsystem(subsystem)         # include information on species 
model.add_instantiation(instantiation) # include information on molecule releases

model.initialize()                     # initialize simulation state 
model.run_iterations(10)               # simulate 10 iterations 
model.end_simulation()                 # final simulation step


# does not check anything
