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

rxn = model.find_reaction_rule('rxn')
assert(rxn)

var_rate_react_a_plus_b = [
  [0, 0],
  [1e-05, 9.98334e+06],
  [2e-05, 1.98669e+07],
  [3e-05, 2.9552e+07],
  [4e-05, 3.89418e+07],
  [5e-05, 4.79426e+07],
  [6e-05, 5.64642e+07]
]
rxn.variable_rate = var_rate_react_a_plus_b
# ---- configuration ----

model.config.total_iterations = ITERATIONS

model.initialize()

#model.dump_internal_state()

model.run_iterations(ITERATIONS)
model.end_simulation()
