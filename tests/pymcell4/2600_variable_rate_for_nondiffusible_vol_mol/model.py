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
    every_n_timesteps = 1
)
model.add_viz_output(viz_output)

# ---- configuration ----

model.config.time_step = parameters.TIME_STEP
model.config.seed = parameters.SEED
model.config.total_iterations = parameters.ITERATIONS

model.notifications.rxn_and_species_report = False

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.2

# the original implementatiton failed also because of species cleanup
model.config.species_cleanup_periodicity = 9


model.initialize()

# run a few iterations first so that the molecules are created before
# the rate is set
model.run_iterations(10)
        
# set rate
rxn = model.find_reaction_rule('a_to_a_b')
assert rxn
rxn.fwd_rate = 5e4

model.run_iterations(1)

# and change it again
rxn.fwd_rate = 1e5

# and run a few more iterations
model.run_iterations(20)
    
model.end_simulation()

