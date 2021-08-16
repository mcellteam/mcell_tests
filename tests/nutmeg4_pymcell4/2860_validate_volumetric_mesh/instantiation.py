# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *
from subsystem import *
from geometry import *
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))


# ---- instantiation ----

# ---- release sites ----

# ---- surface classes assignment ----

# ---- compartments assignment ----

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
#instantiation.add_geometry_object(Cube1)
#instantiation.add_geometry_object(Cube2)
instantiation.add_geometry_object(Outer)

# load seed species information from bngl file
instantiation.load_bngl_compartments_and_seed_species(os.path.join(MODEL_PATH, 'model.bngl'), None, shared.parameter_overrides)

