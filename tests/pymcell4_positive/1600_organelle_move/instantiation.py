import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----

rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = m.Complex('a'),
    region = Cell - (Organelle_1 + Organelle_2),
    number_to_release = 2000
)

rel_b = m.ReleaseSite(
    name = 'rel_b',
    complex = m.Complex('b'),
    region = Organelle_1,
    number_to_release = 1000
)

rel_t1 = m.ReleaseSite(
    name = 'rel_t1',
    complex = m.Complex('t1', orientation = m.Orientation.UP),
    region = Organelle_1_top,
    number_to_release = 700
)

rel_t2 = m.ReleaseSite(
    name = 'rel_t2',
    complex = m.Complex('t2', orientation = m.Orientation.UP),
    region = Organelle_2_top,
    number_to_release = 700
)

# ---- surface classes assignment ----


# ---- compartments assignment ----

# ---- instantiation data ----

instantiation = m.InstantiationData()
instantiation.add_geometry_object(Cell)
instantiation.add_geometry_object(Organelle_2)
instantiation.add_geometry_object(Organelle_1)
instantiation.add_release_site(rel_a)
instantiation.add_release_site(rel_b)
instantiation.add_release_site(rel_t1)
instantiation.add_release_site(rel_t2)
