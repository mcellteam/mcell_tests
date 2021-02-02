#!/usr/bin/env python3

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

from parameters import *

if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value of seed defined in module parameters
    update_seed(int(sys.argv[2]))

import subsystem
import instantiation
import observables

# create main model object
model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = get_seed()
model.config.total_iterations = ITERATIONS

model.notifications.rxn_and_species_report = True

model.config.partition_dimension = 20.02
model.config.subpartition_dimension = 2.002

# ---- default configuration overrides ----


# ---- add components ----

model.add_subsystem(subsystem.subsystem)
model.add_instantiation(instantiation.instantiation)
model.add_observables(observables.observables)

# ---- initialization and execution ----
def rxn_callback(rxn_info, model):
    #print(rxn_info)
    
    # release molecules
    rel_a = m.ReleaseSite(
        name = 'rel_c',
        complex = subsystem.c.inst(),
        shape = m.Shape.SPHERICAL,
        # MCell3 uses the location as offset
        location = (rxn_info.pos3d + m.Vec3(0.005, 0, 0)).to_list(),
        site_diameter = 0,
        number_to_release = 10,
        release_time = rxn_info.time
    )
    model.release_molecules(rel_a)
    
model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()


# sending model as context
model.register_reaction_callback(
    rxn_callback, model, subsystem.react_a_and_b 
)

model.run_iterations(ITERATIONS)
model.end_simulation()
