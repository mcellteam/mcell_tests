import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----

Tetrahedron_rel = m.ReleaseSite(
    name = 'Tetrahedron_rel',
    complex = sm.inst(orientation = m.Orientation.UP),
    region = Tetrahedron,
    number_to_release = 10
)

# ---- surface classes assignment ----


# ---- instantiation data ----

instantiation = m.InstantiationData()
instantiation.add_geometry_object(Tetrahedron)
instantiation.add_release_site(Tetrahedron_rel)
