import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----

rel_a1 = m.ReleaseSite(
    name = 'rel_a1',
    complex = m.Complex('a'),
    shape = m.Shape.SPHERICAL,
    location = (0, 0, 0),
    site_diameter = 0,
    number_to_release = 20
)

rel_a2 = m.ReleaseSite(
    name = 'rel_a2',
    complex = m.Complex('a'),
    shape = m.Shape.SPHERICAL,
    location = (0.14999999999999999, 0, 0),
    site_diameter = 0,
    number_to_release = 20
)

rel_a3 = m.ReleaseSite(
    name = 'rel_a3',
    complex = m.Complex('a'),
    shape = m.Shape.SPHERICAL,
    location = (0.25, 0, 0),
    site_diameter = 0,
    number_to_release = 20
)

rel_a4 = m.ReleaseSite(
    name = 'rel_a4',
    complex = m.Complex('a'),
    shape = m.Shape.SPHERICAL,
    location = (0.35000000000000003, 0, 0),
    site_diameter = 0,
    number_to_release = 20
)

rel_b2 = m.ReleaseSite(
    name = 'rel_b2',
    complex = m.Complex('b'),
    region = Cube3,
    number_to_release = 200
)

# ---- surface classes assignment ----

#Cube1.surface_class = transp
#Cube2.surface_class = transp
#Cube3.surface_class = transp

# ---- compartments assignment ----

# ---- instantiation data ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(Cube1)
instantiation.add_geometry_object(Cube2)
instantiation.add_geometry_object(Cube3)
instantiation.add_release_site(rel_a1)
instantiation.add_release_site(rel_a2)
instantiation.add_release_site(rel_a3)
instantiation.add_release_site(rel_a4)
instantiation.add_release_site(rel_b2)
