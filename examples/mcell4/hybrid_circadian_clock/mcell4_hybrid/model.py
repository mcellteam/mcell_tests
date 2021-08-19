#!/usr/bin/env python3

import sys
import os
import importlib.util

ONLY_BNGL_EXPORT = False

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
model.notifications.rxn_and_species_report = False
model.notifications.rxn_probability_changed = False
#model.notifications.iteration_report = True

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.5

model.config.reaction_class_cleanup_periodicity = 0
model.config.species_cleanup_periodicity = 0

# ---- add components ----

import subsystem
import instantiation
import observables

model.add_subsystem(subsystem.subsystem)
model.add_instantiation(instantiation.instantiation)
model.add_observables(observables.observables)

# ---- default configuration overrides ----

if customization and 'custom_config' in dir(customization):
    # user-defined model configuration
    customization.custom_config(model)


# molecule counts
count_A = model.find_count('A')
assert count_A
count_AR = model.find_count('AR')
assert count_AR
count_mRNA_R = model.find_count('mRNA_R')
assert count_mRNA_R

# reactions
rxn_A_to_AR = model.find_reaction_rule('A_to_AR')
assert rxn_A_to_AR
rxn_AR_to_0 = model.find_reaction_rule('AR_to_0')
assert rxn_AR_to_0

# reaction counts
count_A_to_AR = m.Count(
    name = "count_A_to_AR",
    expression = m.CountTerm(
        reaction_rule = rxn_A_to_AR
    ),
    every_n_timesteps = 0 
)

count_AR_to_0 = m.Count(
    name = "count_AR_to_0",
    expression = m.CountTerm(
        reaction_rule = rxn_AR_to_0
    ),
    every_n_timesteps = 0 
)

model.add_count(count_A_to_AR)
model.add_count(count_AR_to_0)

# ---- initialization and execution ----
model.initialize()

if DUMP:
    model.dump_internal_state()


ODE_UPDATE_INTERVAL = 1  # time steps
VOLUME = 4.1889930549057564 * 1e-15 # l


def dR(dt, dR_due_A_to_AR, dR_due_AR_to_0, num_R, num_AR):
    # dt - in [s]
    # num_mRNA_R - copy number
    # 
    # original reactions
    # A + R -> AR 1204 * uM_1_to_M_1 [1/M*1/s]
    #   -> R -> 0 rate depends on A -> same as 
    # R -> 0 0.2 [1/s]
    # mRNA_R -> mRNA_R + R  5 [1/s]
    # AR -> R 1
    #
    # how the amount of R should change (in copy number, float) 
    res = \
        +dR_due_A_to_AR \
        -(num_R * 0.2 * dt) \
        +(num_mRNA_R * 5 * dt) \
        +dR_due_AR_to_0
    
    #print("dR", res)
    return res


def compute_A_to_AR_rate(num_R):
    # num_R - copy number (as float) - internally kept as 
    #         float but the rate computation uses an integer value of it
    #
    # original reaction: A + R -> AR 1204 * 1e6 [1/M*1/s]
    # changed to: A -> R rate(num_R)
    #
    num_R_copy_nr = int(num_R)
    
    rate = (1204 * 1e6) # 1/M*1/s 
    
    # N -> M 
    conc_R = num_R_copy_nr / NA / VOLUME  # M
    res = rate * conc_R # 1/s
    #print("A_to_AR_rate", res)
    return res




NA = 6.0221409e+23

num_R = 0.0 # initial value, model as float

r_dat = open('./react_data/seed_' + str(SEED).zfill(5) + '/R.dat', 'w')

rxns_A_to_AR_prev = count_A_to_AR.get_current_value()
assert rxns_A_to_AR_prev == 0
rxns_AR_to_0_prev = count_AR_to_0.get_current_value()
assert rxns_AR_to_0_prev == 0

for i in range(int(ITERATIONS/ODE_UPDATE_INTERVAL)):
    
    model.run_iterations(ODE_UPDATE_INTERVAL)
    
    num_A = count_A.get_current_value()
    num_AR = count_AR.get_current_value()
    num_mRNA_R = count_mRNA_R.get_current_value()

    t = i * ODE_UPDATE_INTERVAL * TIME_STEP
        
    # get counts of reactions that affect R
    rxns_A_to_AR_curr = count_A_to_AR.get_current_value()
    dR_due_A_to_AR = -(rxns_A_to_AR_curr - rxns_A_to_AR_prev)
    rxns_A_to_AR_prev = rxns_A_to_AR_curr
    
    rxns_AR_to_0_curr = count_AR_to_0.get_current_value()
    dR_due_AR_to_0 = rxns_AR_to_0_curr - rxns_AR_to_0_prev
    rxns_AR_to_0_prev = rxns_AR_to_0_curr

    #if i % (SAMPLING_PERIODICITY/ODE_UPDATE_INTERVAL) == 0:
    #    print("----\n%.4f" % t)
    #    print("R: %.4f, AR: %.4f, mRNA_R: %4f, A: %.4f" % (num_R, num_AR, num_mRNA_R, num_A))
    #    print("rxns_A_to_AR: %.4f, rxns_AR_to_0: %.4f" % (rxns_A_to_AR_curr, rxns_AR_to_0_curr))
    
    
    num_R += dR(ODE_UPDATE_INTERVAL * TIME_STEP, dR_due_A_to_AR, dR_due_AR_to_0, num_R, num_AR) 

    rate_A_to_R = compute_A_to_AR_rate(num_R)
    rxn_A_to_AR.fwd_rate = rate_A_to_R 

    #if i % (SAMPLING_PERIODICITY/ODE_UPDATE_INTERVAL) == 0:
    #    print("R_new: %.4f" % num_R)
    #    print("rate: %.4f" % rxn_A_to_AR.fwd_rate)


    if i % (SAMPLING_PERIODICITY/ODE_UPDATE_INTERVAL) == 0:
        r_dat.write("%.4f %8f\n" % (t, num_R))
        r_dat.flush()
    
    #print("A: " + str(num_A) + ", R: " + str(num_R) + ", AR: " + str(num_AR))
    
r_dat.close()

model.end_simulation()
