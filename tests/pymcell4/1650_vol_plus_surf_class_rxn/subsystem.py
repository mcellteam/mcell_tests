# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *

# ---- subsystem ----

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

empty = m.SurfaceClass(
    name = 'empty',
    type = m.SurfacePropertyType.REACTIVE
)

unnamed_reaction_rule_0 = m.ReactionRule(
    name = 'unnamed_reaction_rule_0',
    reactants = [ m.Complex('vol1', orientation = m.Orientation.DOWN), m.Complex('empty', orientation = m.Orientation.UP) ],
    products = [ m.Complex('vol2', orientation = m.Orientation.UP) ],
    fwd_rate = 1e7
)

# ---- create subsystem object and add components ----

subsystem = m.Subsystem()
subsystem.add_surface_class(empty)
subsystem.add_reaction_rule(unnamed_reaction_rule_0)

# load subsystem information from bngl file
subsystem.load_bngl_molecule_types_and_reaction_rules(os.path.join(MODEL_PATH, 'model.bngl'), shared.parameter_overrides)

# set additional information about species and molecule types that cannot be stored in BNGL,
# elementary molecule types are already in the subsystem after they were loaded from BNGL
def set_bngl_molecule_types_info(subsystem):
    vol1 = subsystem.find_elementary_molecule_type('vol1')
    assert vol1, "Elementary molecule type 'vol1' was not found"
    vol1.diffusion_constant_3d = 1e-5

    vol2 = subsystem.find_elementary_molecule_type('vol2')
    assert vol2, "Elementary molecule type 'vol2' was not found"
    vol2.diffusion_constant_3d = 1e-6

set_bngl_molecule_types_info(subsystem)
