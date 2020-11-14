#!/usr/bin/env python3

import sys
import os
import copy
import numpy as np

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

ITERATIONS = 1

from geometry import *
from observables import *

model = m.Model()

model.add_observables(observables)

model.add_geometry_object(Compartment)

# molecules in test.bngl are released into 'Compartment'
model.load_bngl('test.bngl')
    
model.config.total_iterations_hint = ITERATIONS
    
model.initialize()
    
#model.dump_internal_state()
    
model.run_iterations(ITERATIONS)

model.end_simulation()


