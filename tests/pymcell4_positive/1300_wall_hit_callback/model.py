#!/usr/bin/env python3

import sys
import os

MCELL_DIR = os.environ.get('MCELL_DIR', '')
if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'lib'))
else:
    print("Error: variable MCELL_DIR that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

from parameters import *

if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])

import subsystem
import instantiation

model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations_hint = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- default configuration overrides ----

# ---- add components ----

model.add_subsystem(subsystem.subsystem)
model.add_instantiation_data(instantiation.instantiation)

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()


# --------------- test ------------------------

# example class passed as context to the callback
class HitCount():
    def __init__(self):
        self.count = 0

def wall_hit_callback(wall_hit_info, context):
    #print("Wall hit callback called")
    #print(wall_hit_info)
    context.count += 1
    

tetrahedron_object = model.find_geometry_object('Tetrahedron')
assert tetrahedron_object

vm_species = model.find_species('vm')
assert vm_species
assert vm_species == subsystem. vm

context = HitCount()

# the object and species are optional, this simple test contains single
# object and species anyway 
model.register_wall_hit_callback(
    wall_hit_callback, context
    #, tetrahedron_object, vm_species 
)

for i in range(ITERATIONS + 1):
    model.run_iterations(1)

model.end_simulation()

print("Total number of wall hits: " + str(context.count))
assert context.count == 36045

