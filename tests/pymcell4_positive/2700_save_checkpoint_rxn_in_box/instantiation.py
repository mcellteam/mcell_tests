# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----

rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = a.inst(),
    shape = m.Shape.SPHERICAL,
    location = m.Vec3(0, 0, 0),
    site_diameter = 0,
    number_to_release = 100
)

rel_b = m.ReleaseSite(
    name = 'rel_b',
    complex = b.inst(),
    shape = m.Shape.SPHERICAL,
    location = m.Vec3(5.0000000000000001e-03, 0, 0),
    site_diameter = 0,
    number_to_release = 100
)

# ---- surface classes assignment ----

# ---- compartments assignment ----

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(Cube)
instantiation.add_release_site(rel_a)
instantiation.add_release_site(rel_b)
