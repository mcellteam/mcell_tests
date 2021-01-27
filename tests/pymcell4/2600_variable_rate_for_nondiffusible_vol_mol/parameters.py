import mcell as m

# ---- model parameters ----

# load parameters from BNGL
bngl_params = m.bngl_utils.load_bngl_parameters('model.bngl')


VOLUME_UM3 = bngl_params['VOLUME_UM3']

# ---- simulation setup ----

ITERATIONS = 100
TIME_STEP = 1e-06
DUMP = False
EXPORT_DATA_MODEL = True
SEED = 1
