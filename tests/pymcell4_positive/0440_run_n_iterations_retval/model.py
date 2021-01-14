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

# create main model object (empty)
model = m.Model()

# ---- configuration ----

model.config.time_step = 1e-6
model.config.seed = 1
model.config.total_iterations = 10

# ---- initialization and execution ----

model.initialize()

res1 = model.run_iterations(1)
assert res1 == 1

res2 = model.run_iterations(5)
assert res2 == 5

model.end_simulation()
