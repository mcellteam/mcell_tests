#!/usr/bin/env python3

import sys
import os
import math
import copy

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

from parameters import *

if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])


model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = 1
model.config.total_iterations = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- default configuration overrides ----

# ---- add components ----

model.load_bngl('model.bngl')

model2 = copy.deepcopy(model)
model2.config.seed = 4

# ---- initialization and execution ----

model.initialize()
model2.initialize()

model.run_iterations(ITERATIONS)
model2.run_iterations(ITERATIONS)


print(model.find_count('c').get_current_value())
assert model.find_count('c').get_current_value() == 34

print(model2.find_count('c').get_current_value())
assert model2.find_count('c').get_current_value() == 25
