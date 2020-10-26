import mcell as m

# ---- model parameters ----

reaction_rate = 1e9


# ---- simulation setup ----

ITERATIONS = 1000
TIME_STEP = 1e-6
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

