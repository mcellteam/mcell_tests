# ---- model parameters ----

# ---- simulation setup ----

ITERATIONS = 
TIME_STEP = 
DUMP = False
EXPORT_DATA_MODEL = True

# do not use the variable SEED_MODULE_LOCAL directly,
# Python on import creates copies that do not reflect the current value
SEED_MODULE_LOCAL = 1

def update_seed(new_value):
    global SEED_MODULE_LOCAL
    SEED_MODULE_LOCAL = new_value

def get_seed():
    return SEED_MODULE_LOCAL

