import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

rel_a = m.ReleaseSite(
    name = 'rel_a',
    species = a,
    shape = m.Shape.Spherical,
    location = m.Vec3(0, 0, 0),
    number_to_release = 100
)

rel_b = m.ReleaseSite(
    name = 'rel_b',
    species = b,
    shape = m.Shape.Spherical,
    location = m.Vec3(5.00000000000000010e-03, 0, 0),
    number_to_release = 100
)

instantiation = m.InstantiationData()
instantiation.add_geometry_object(Cube)
instantiation.add_release_site(rel_a)
instantiation.add_release_site(rel_b)
