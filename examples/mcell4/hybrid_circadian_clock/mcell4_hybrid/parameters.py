# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import sys
import os
import math
import shared
import mcell as m

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

# ---- model parameters ----

# declare all items from parameter_overrides as variables
for parameter_name, value in shared.parameter_overrides.items():
    setattr(sys.modules[__name__], parameter_name, value)

# auxiliary function used to determine whether a parameter was defined
def not_defined(parameter_name):
    return parameter_name not in globals()

# load parameters from BNGL
bngl_params = m.bngl_utils.load_bngl_parameters(os.path.join(MODEL_PATH, 'model.bngl'), shared.parameter_overrides)


unimol_mult = bngl_params['unimol_mult']  

# ---- simulation setup ----

if not_defined('TIME_STEP'):
    TIME_STEP = 5e-7  

if not_defined('ITERATIONS'):
    ITERATIONS = int(0.25/TIME_STEP) # how many seconds? 45/30 * 1.5?, new: 45/270


if not_defined('DUMP'):
    DUMP = False

if not_defined('EXPORT_DATA_MODEL'):
    EXPORT_DATA_MODEL = False

if not_defined('SEED'):
    SEED = 1


SAMPLING_PERIODICITY = 200 # warning: time_step dependent
