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
# load the information on species (diffusion constants) and reaction rules  
subsystem.load_bngl_molecule_types_and_reaction_rules('example.bngl')

instantiation = m.Instantiation()
# create compartment CP and create release sites for moelcules A and B
instantiation.load_bngl_compartments_and_seed_species('example.bngl')

model = m.Model()
model.add_subsystem(subsystem)         # include species A, B, C, and reaction rule 
model.add_instantiation(instantiation) # include object CP and molecule releases information

model.initialize()                     # initialize simulation state 
model.run_iterations(10)               # simulate 10 iterations 
model.end_simulation()                 # final simulation step


# does not check anything
