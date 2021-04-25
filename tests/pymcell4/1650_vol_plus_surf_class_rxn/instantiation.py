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

Plane.surface_class = empty
# ---- compartments assignment ----

vol1_rel = m.ReleaseSite(
    name = 'vol1_rel',
    complex = m.Complex('vol1'),
    region = Cube,
    number_to_release = 2000
)

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(Plane)
instantiation.add_geometry_object(Cube)
instantiation.add_release_site(vol1_rel)

# load seed species information from bngl file
instantiation.load_bngl_compartments_and_seed_species(os.path.join(MODEL_PATH, 'model.bngl'), None, shared.parameter_overrides)

