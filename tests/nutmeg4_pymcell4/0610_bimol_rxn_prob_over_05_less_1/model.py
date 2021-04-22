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


params = m.bngl_utils.load_bngl_parameters('test.bngl')

ITERATIONS = int(params['ITERATIONS'])

DUMP = True
EXPORT_DATA_MODEL = True


# ---- load bngl file ----

model = m.Model()

model.load_bngl('test.bngl')


# ---- configuration ----

model.config.total_iterations = ITERATIONS
model.warnings.high_reaction_probability = m.WarningLevel.WARNING


model.initialize()
model.run_iterations(ITERATIONS)
model.end_simulation()
