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

box_bottom.surface_class = reflect_edge
# ---- compartments assignment ----

rel_m = m.ReleaseSite(
    name = 'rel_m',
    complex = m.Complex('M'),
    region = box_bottom,
    number_to_release = 3755
)

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(box)
instantiation.add_release_site(rel_m)

# load seed species information from bngl file
instantiation.load_bngl_compartments_and_seed_species(os.path.join(MODEL_PATH, 'model.bngl'), None, shared.parameter_overrides)

