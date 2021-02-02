import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----

rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = vm,
    shape = m.Shape.SPHERICAL,
    location = (0, 0, 0),
    site_diameter = 0,
    number_to_release = 100
)

# ---- surface classes assignment ----


# ---- instantiation data ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(Tetrahedron)
instantiation.add_release_site(rel_a)
