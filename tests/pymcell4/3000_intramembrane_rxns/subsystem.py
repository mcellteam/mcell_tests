# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

from parameters import *

# ---- subsystem ----

# ---- create subsystem object and add components ----

subsystem = m.Subsystem()

# load subsystem information from bngl file
subsystem.load_bngl_molecule_types_and_reaction_rules('model.bngl')

# set additional information about species and molecule types that cannot be stored in BNGL,
# elementary molecule types are already in the subsystem after they were loaded from BNGL
def set_bngl_molecule_types_info(subsystem):
    A = subsystem.find_elementary_molecule_type('A')
    assert A, "Elementary molecule type 'A' was not found"
    A.diffusion_constant_2d = 1e-4

    B = subsystem.find_elementary_molecule_type('B')
    assert B, "Elementary molecule type 'B' was not found"
    B.diffusion_constant_2d = 1e-4

    C = subsystem.find_elementary_molecule_type('C')
    assert C, "Elementary molecule type 'C' was not found"
    C.diffusion_constant_2d = 1e-4

    D = subsystem.find_elementary_molecule_type('D')
    assert D, "Elementary molecule type 'D' was not found"
    D.diffusion_constant_2d = 1e-4

set_bngl_molecule_types_info(subsystem)
