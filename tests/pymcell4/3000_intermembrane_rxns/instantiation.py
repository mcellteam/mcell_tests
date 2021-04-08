# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----

rel_A = m.ReleaseSite(
    name = 'rel_A',
    complex = m.Complex('A', orientation = m.Orientation.UP),
    region = up,
    number_to_release = 100
)

rel_B = m.ReleaseSite(
    name = 'rel_B',
    complex = m.Complex('B', orientation = m.Orientation.UP),
    region = bottom,
    number_to_release = 100
)

# ---- surface classes assignment ----

# ---- compartments assignment ----

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(up)
instantiation.add_geometry_object(bottom)
instantiation.add_release_site(rel_A)
instantiation.add_release_site(rel_B)
