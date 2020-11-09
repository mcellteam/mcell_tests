import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----

# ---- surface classes assignment ----

Cube_left_side.surface_class = cclamp_left
Cube_right_side.surface_class = cclamp_right

# ---- compartments assignment ----

# ---- instantiation data ----

instantiation = m.InstantiationData()
instantiation.add_geometry_object(Cube)
