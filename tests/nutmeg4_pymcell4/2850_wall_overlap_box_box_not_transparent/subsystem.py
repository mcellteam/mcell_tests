# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *

# ---- subsystem ----

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

# ---- create subsystem object and add components ----

subsystem = m.Subsystem()

# load subsystem information from bngl file
subsystem.load_bngl_molecule_types_and_reaction_rules(os.path.join(MODEL_PATH, 'model.bngl'), shared.parameter_overrides)

# set additional information about species and molecule types that cannot be stored in BNGL,
# elementary molecule types are already in the subsystem after they were loaded from BNGL
def set_bngl_molecule_types_info(subsystem):
    a = subsystem.find_elementary_molecule_type('a')
    assert a, "Elementary molecule type 'a' was not found"
    a.diffusion_constant_3d = 1e-4

    b = subsystem.find_elementary_molecule_type('b')
    assert b, "Elementary molecule type 'b' was not found"
    b.diffusion_constant_3d = 1e-4

set_bngl_molecule_types_info(subsystem)
