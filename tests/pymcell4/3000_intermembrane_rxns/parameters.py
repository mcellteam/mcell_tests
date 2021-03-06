# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

# ---- model parameters ----

# load parameters from BNGL
bngl_params = m.bngl_utils.load_bngl_parameters('model.bngl')


# ---- simulation setup ----

ITERATIONS = 100
TIME_STEP = 1e-6
DUMP = False
EXPORT_DATA_MODEL = True
SEED = 1 # may be overwritten based on commandline arguments

