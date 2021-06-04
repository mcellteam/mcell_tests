#!/usr/bin/env python3

import sys
import os
import importlib.util

ONLY_BNGL_EXPORT = True

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))


# ---- import mcell module located in directory specified by system variable MCELL_PATH  ----

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


# ---- customization and argument processing ----

# this module is used to hold any overrides of parameter values
import shared
# import the customization.py module if it exists
if os.path.exists(os.path.join(MODEL_PATH, 'customization.py')):
    import customization
else:
    customization = None

# process command-line arguments
if customization and 'custom_argparse_and_parameters' in dir(customization):
    # custom argument processing and parameter setup
    customization.custom_argparse_and_parameters()
else:
    if len(sys.argv) == 1:
        # no arguments
        pass
    elif len(sys.argv) == 3 and sys.argv[1] == '-seed':
        # overwrite value of seed defined in module parameters
        shared.parameter_overrides['SEED'] = int(sys.argv[2])
    else:
        print("Error: invalid command line arguments")
        print("  usage: " + sys.argv[0] + "[-seed N]")
        sys.exit(1)


# the module parameters uses shared.parameter_overrides to override parameter values
from parameters import *


# resume simulation if a checkpoint was created
checkpoint_dir = m.run_utils.get_last_checkpoint_dir(SEED)
if checkpoint_dir:
    # change sys.path so that the only the checkpointed files are loaded
    sys.path = m.run_utils.remove_cwd(sys.path)
    sys.path.append(checkpoint_dir)
    
    # prepare import of the 'model' module from the checkpoint
    model_spec = importlib.util.spec_from_file_location(
        'model', os.path.join(checkpoint_dir, 'model.py'))
    model_module = importlib.util.module_from_spec(model_spec)
    
    # run import, this also resumes simulation from the checkpoint
    model_spec.loader.exec_module(model_module)

    # exit after simulation has finished successfully
    sys.exit(0)


# ---- model creation and simulation ----

# create main model object
model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS

model.warnings.high_reaction_probability = m.WarningLevel.IGNORE
model.notifications.rxn_and_species_report = True
model.notifications.rxn_probability_changed = True

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.05

# ---- default configuration overrides ----

if customization and 'custom_config' in dir(customization):
    # user-defined model configuration
    customization.custom_config(model)

# ---- add components ----

import subsystem
import instantiation
import observables

model.add_subsystem(subsystem.subsystem)
model.add_instantiation(instantiation.instantiation)
model.add_observables(observables.observables)

# ---- initialization and execution ----
model.initialize()

if DUMP:
    model.dump_internal_state()


ODE_UPDATE_PERIODICITY = 100  # time steps
VOLUME = 4.1889930549057564 * 1e-15 # um^3


def dR(dt, num_mRNA_R):
    # dt - in [s]
    # num_mRNA_R - copy number
    # 
    # original reactions
    # R -> 0 0.2 [1/s]
    # mRNA_R -> mRNA_R + R  5 [1/s]
    #
    # TODO 
    return 0


def compute_A_to_AR_rate(num_R):
    # num_R - copy number (as float)
    #
    # original reaction: A + R -> AR 1204 * uM_1_to_M_1 [1/M*1/s]
    # changed to: A -> R rate(num_R)
    #
    # TODO
    return 0


count_A = model.find_count('A')
assert count_A
count_AR = model.find_count('AR')
assert count_AR
count_mRNA_R = model.find_count('mRNA_R')
assert count_mRNA_R
rxn_A_to_AR = model.find_reaction_rule('A_to_AR')
assert rxn_A_to_AR

num_R = 0.0 # initial value, model as float

for i in range(int(ITERATIONS/ODE_UPDATE_PERIODICITY)):
    
    model.run_iterations(ODE_UPDATE_PERIODICITY)
    
    num_R += dR(ODE_UPDATE_PERIODICITY * TIME_STEP, count_mRNA_R.get_current_value()) 

    rxn_A_to_AR.fwd_rate = compute_A_to_AR_rate(num_R)

    num_A = count_A.get_current_value()
    num_AR = count_AR.get_current_value()

    print("A: " + str(num_A) + ", R: " + str(num_R) + ", AR: " + str(num_AR))
    


model.end_simulation()
