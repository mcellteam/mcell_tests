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

var_rate_react_a_to_b_0 = [
  [0, 0],
  [3e-06, 2955.2],
  [4e-06, 3894.18],
  [5e-06, 4794.26],
  [8e-06, 7173.56],
  [9e-06, 7833.27],
  [1e-05, 8414.71],
  [2.2e-05, 8084.96],
  [2.3e-05, 7457.05],
  [2.4e-05, 6754.63],
  [3.4e-05, 2555.41],
  [3.5e-05, 3507.83],
  [3.6e-05, 4425.2],
  [3.7e-05, 5298.36],
  [3.8e-05, 6118.58],
  [3.9e-05, 6877.66],
  [4.9e-05, 9824.53],
  [5e-05, 9589.24],
  [5.8e-05, 4646.02],
  [6e-05, 2794.15],
  [6.1e-05, 1821.63],
  [6.2e-05, 830.89]
] 

