# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *
from subsystem import *
from geometry import *
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))


box1_only_rel = m.ReleaseSite(
    name = 'box1_only_rel',
    complex = vm.inst(),
    region = box1 - box2,
    number_to_release = 4
)

box2_only_rel = m.ReleaseSite(
    name = 'box2_only_rel',
    complex = vm.inst(),
    region = box2 - box1,
    number_to_release = 6
)

both_only_rel = m.ReleaseSite(
    name = 'both_only_rel',
    complex = vm.inst(),
    region = box1 * box2,
    number_to_release = 8
)

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(box1)
instantiation.add_geometry_object(box2)
instantiation.add_release_site(box1_only_rel)
instantiation.add_release_site(box2_only_rel)
instantiation.add_release_site(both_only_rel)
