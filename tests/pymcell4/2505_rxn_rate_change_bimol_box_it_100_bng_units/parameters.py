import mcell as m

# ---- model parameters ----

# load parameters from BNGL
bngl_params = m.bngl_utils.load_bngl_parameters('model.bngl')


# ---- simulation setup ----

ITERATIONS = 100
TIME_STEP = 1e-06
DUMP = False
EXPORT_DATA_MODEL = True

# do not use the variable module_seed_value directly,
# Python on import creates copies that do not reflect the current value
module_seed_value = 1

def update_seed(new_value):
    global module_seed_value
    module_seed_value = new_value

def get_seed():
    return module_seed_value


# ---- variable rate ----
NA_UM3 = 6.0221409e8

var_rate_react_a_plus_b_0 = [
  [0, 0/NA_UM3],
  [1e-06, 9.98334e+06/NA_UM3],
  [2e-06, 1.98669e+07/NA_UM3],
  [3e-06, 2.9552e+07/NA_UM3],
  [4e-06, 3.89418e+07/NA_UM3],
  [5e-06, 4.79426e+07/NA_UM3],
  [6e-06, 5.64642e+07/NA_UM3],
  [7e-06, 6.44218e+07/NA_UM3],
  [8e-06, 7.17356e+07/NA_UM3],
  [9e-06, 7.83327e+07/NA_UM3],
  [1e-05, 8.41471e+07/NA_UM3],
  [1.1e-05, 8.91207e+07/NA_UM3],
  [1.2e-05, 9.32039e+07/NA_UM3],
  [1.3e-05, 9.63558e+07/NA_UM3],
  [1.4e-05, 9.8545e+07/NA_UM3],
  [1.5e-05, 9.97495e+07/NA_UM3],
  [1.6e-05, 9.99574e+07/NA_UM3],
  [1.7e-05, 9.91665e+07/NA_UM3],
  [1.8e-05, 9.73848e+07/NA_UM3],
  [1.9e-05, 9.463e+07/NA_UM3],
  [2e-05, 9.09297e+07/NA_UM3],
  [2.1e-05, 8.63209e+07/NA_UM3],
  [2.2e-05, 8.08496e+07/NA_UM3],
  [2.3e-05, 7.45705e+07/NA_UM3],
  [2.4e-05, 6.75463e+07/NA_UM3],
  [2.5e-05, 5.98472e+07/NA_UM3],
  [2.6e-05, 5.15501e+07/NA_UM3],
  [2.7e-05, 4.2738e+07/NA_UM3],
  [2.8e-05, 3.34988e+07/NA_UM3],
  [2.9e-05, 2.39249e+07/NA_UM3],
  [3e-05, 1.4112e+07/NA_UM3],
  [3.1e-05, 4.15807e+06/NA_UM3],
  [3.2e-05, 5.83741e+06/NA_UM3],
  [3.3e-05, 1.57746e+07/NA_UM3],
  [3.4e-05, 2.55541e+07/NA_UM3],
  [3.5e-05, 3.50783e+07/NA_UM3],
  [3.6e-05, 4.4252e+07/NA_UM3],
  [3.7e-05, 5.29836e+07/NA_UM3],
  [3.8e-05, 6.11858e+07/NA_UM3],
  [3.9e-05, 6.87766e+07/NA_UM3],
  [4e-05, 7.56802e+07/NA_UM3],
  [4.1e-05, 8.18277e+07/NA_UM3],
  [4.2e-05, 8.71576e+07/NA_UM3],
  [4.3e-05, 9.16166e+07/NA_UM3],
  [4.4e-05, 9.51602e+07/NA_UM3],
  [4.5e-05, 9.7753e+07/NA_UM3],
  [4.6e-05, 9.93691e+07/NA_UM3],
  [4.7e-05, 9.99923e+07/NA_UM3],
  [4.8e-05, 9.96165e+07/NA_UM3],
  [4.9e-05, 9.82453e+07/NA_UM3],
  [5e-05, 9.58924e+07/NA_UM3],
  [5.1e-05, 9.25815e+07/NA_UM3],
  [5.2e-05, 8.83455e+07/NA_UM3],
  [5.3e-05, 8.32267e+07/NA_UM3],
  [5.4e-05, 7.72764e+07/NA_UM3],
  [5.5e-05, 7.0554e+07/NA_UM3],
  [5.6e-05, 6.31267e+07/NA_UM3],
  [5.7e-05, 5.50686e+07/NA_UM3],
  [5.8e-05, 4.64602e+07/NA_UM3],
  [5.9e-05, 3.73877e+07/NA_UM3],
  [6e-05, 2.79415e+07/NA_UM3],
  [6.1e-05, 1.82163e+07/NA_UM3],
  [6.2e-05, 8.30894e+06/NA_UM3]
] # var_rate_react_a_plus_b_0

