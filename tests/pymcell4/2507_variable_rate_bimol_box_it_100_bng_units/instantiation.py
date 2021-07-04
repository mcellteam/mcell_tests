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

rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = m.Complex('a'),
    shape = m.Shape.SPHERICAL,
    location = (0, 0, 0),
    site_diameter = 0,
    number_to_release = 1000
)

rel_b = m.ReleaseSite(
    name = 'rel_b',
    complex = m.Complex('b'),
    shape = m.Shape.SPHERICAL,
    location = (5.0000000000000001e-03, 0, 0),
    site_diameter = 0,
    number_to_release = 1000
)

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(Cube)
instantiation.add_release_site(rel_a)
instantiation.add_release_site(rel_b)

# load seed species information from bngl file
instantiation.load_bngl_compartments_and_seed_species(os.path.join(MODEL_PATH, 'model.bngl'), None, shared.parameter_overrides)

