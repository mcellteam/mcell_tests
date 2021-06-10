# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *
from subsystem import *
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))


# ---- instantiation ----

# ---- release sites ----

# ---- surface classes assignment ----

box = m.geometry_utils.create_box('box', 0.14422)
box.is_bngl_compartment = True

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(box)

# load seed species information from bngl file
instantiation.load_bngl_compartments_and_seed_species(os.path.join(MODEL_PATH, 'model.bngl'), None, shared.parameter_overrides)

