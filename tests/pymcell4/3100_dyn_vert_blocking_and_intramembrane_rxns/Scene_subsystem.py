# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import mcell as m

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

from Scene_parameters import *

# ---- subsystem ----

lipid_raft_A = m.SurfaceClass(
    name = 'lipid_raft_A',
    type = m.SurfacePropertyType.REFLECTIVE,
    affected_complex_pattern = m.Complex('A')
)

lipid_raft_B = m.SurfaceClass(
    name = 'lipid_raft_B',
    type = m.SurfacePropertyType.REFLECTIVE,
    affected_complex_pattern = m.Complex('B')
)

# ---- create subsystem object and add components ----

subsystem = m.Subsystem()
subsystem.add_surface_class(lipid_raft_A)
subsystem.add_surface_class(lipid_raft_B)

# load subsystem information from bngl file
subsystem.load_bngl_molecule_types_and_reaction_rules(os.path.join(MODEL_PATH, 'Scene_model.bngl'))

# set additional information about species and molecule types that cannot be stored in BNGL,
# elementary molecule types are already in the subsystem after they were loaded from BNGL
def set_bngl_molecule_types_info(subsystem):
    A = subsystem.find_elementary_molecule_type('A')
    assert A, "Elementary molecule type 'A' was not found"
    A.diffusion_constant_3d = 0

    B = subsystem.find_elementary_molecule_type('B')
    assert B, "Elementary molecule type 'B' was not found"
    B.diffusion_constant_3d = 0

set_bngl_molecule_types_info(subsystem)
