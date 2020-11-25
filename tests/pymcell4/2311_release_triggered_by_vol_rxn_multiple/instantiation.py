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
    number_to_release = 20
)

rel_b = m.ReleaseSite(
    name = 'rel_b',
    complex = b.inst(),
    shape = m.Shape.SPHERICAL,
    location = m.Vec3(0.02, 0, 0),
    site_diameter = 0,
    number_to_release = 20
)

# ---- surface classes assignment ----


# ---- compartments assignment ----

# ---- instantiation data ----

instantiation = m.InstantiationData()
instantiation.add_geometry_object(Cube)
instantiation.add_release_site(rel_a)
instantiation.add_release_site(rel_b)
