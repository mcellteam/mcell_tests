#!/usr/bin/env python3

# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import sys
import os

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

# ---- import mcell module located in directory ----
# ---- specified by system variable MCELL_PATH  ----
MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    if os.path.exists(os.path.join(lib_path, 'mcell.so')) or \
        os.path.exists(os.path.join(lib_path, 'mcell.dll')):
        sys.path.append(lib_path)
    else:
        print("Error: Python module mcell.so or mcell.dll was not found in "
              "directory '" + lib_path + "' constructed from system variable "
              "MCELL_PATH.")
        sys.exit(1)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)

import mcell as m

import parameters

if len(sys.argv) == 1:
    # no arguments
    pass
elif len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value of seed defined in module parameters
    parameters.SEED = int(sys.argv[2])
else:
    print("Error: invalid command line arguments")
    print("  usage: " + sys.argv[0] + "[-seed N]")
    sys.exit(1)


# create main model object
model = m.Model()

model.load_bngl('model.bngl', './react_data/seed_' + str(parameters.SEED).zfill(5) + '/')

viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(parameters.SEED).zfill(5) + '/Scene',
    every_n_timesteps = 100
)
model.add_viz_output(viz_output)

# ---- configuration ----

model.config.time_step = parameters.TIME_STEP
model.config.seed = parameters.SEED
model.config.total_iterations_hint = parameters.ITERATIONS

model.notifications.rxn_and_species_report = False

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.2

model.initialize()

if parameters.DUMP:
    model.dump_internal_state()

if parameters.EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

# Count is an object that defines an observable in the model, 
# with this call to find_count, we get a Count object created from 
# a statement in BNGL's observables section (model.bngl)    
#  Molecules c c
count_c = model.find_count('c')
assert count_c

# here we get the Count object created from 
#  Molecules e e
count_e = model.find_count('e')
assert count_e

# similarly as with the counts above, here we get a ReactionRule object 
# created from BNGL reaction rule
#  d_to_e: d -> e 0
rxn_d_to_e = model.find_reaction_rule('d_to_e')
assert rxn_d_to_e

for i in range(parameters.ITERATIONS):
    
    model.run_iterations(1)
        
    # c_count will contain the nuber of molecules 'c' in the whole world
    # - defined by the observable Molecules c c
    c_count = count_c.get_current_value()  
    
    # in this example, we will simply set the unimol rate equal to the
    # number of molecules
    # setting the fwd_rate attribute causes an internal update function 
    # in MCell to be executed and in this case this updates the
    # times scheduled for unimolecular reactions of all molecules 'd'    
    rxn_d_to_e.fwd_rate = c_count
    
model.end_simulation()

#print("c: " + str(count_c.get_current_value()))
#print("e: " + str(count_e.get_current_value()))
