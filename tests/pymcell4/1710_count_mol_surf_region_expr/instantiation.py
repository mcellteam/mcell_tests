# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *
from subsystem import *
from geometry import *
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))


box1_sr1_rel = m.ReleaseSite(
    name = 'box1_sr1_rel',
    complex = sm.inst(),
    region = box1_sr1,
    number_to_release = 4
)

box1_sr2_rel = m.ReleaseSite(
    name = 'box1_sr2_rel',
    complex = sm.inst(),
    region = box1_sr2,
    number_to_release = 6
)

# TODO: release on difference, union, and intersection

box2_rel = m.ReleaseSite(
    name = 'box2_rel',
    complex = sm.inst(),
    region = box2,
    number_to_release = 8
)

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(box1)
instantiation.add_geometry_object(box2)
instantiation.add_release_site(box1_sr1_rel)
instantiation.add_release_site(box1_sr2_rel)
instantiation.add_release_site(box2_rel)
