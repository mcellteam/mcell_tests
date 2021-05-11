# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *

# ---- subsystem ----

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

reflect_edge = m.SurfaceClass(
    name = 'reflect_edge',
    type = m.SurfacePropertyType.REFLECTIVE,
    affected_complex_pattern = m.AllSurfaceMolecules
)

# ---- create subsystem object and add components ----

subsystem = m.Subsystem()
subsystem.add_surface_class(reflect_edge)

# load subsystem information from bngl file
subsystem.load_bngl_molecule_types_and_reaction_rules(os.path.join(MODEL_PATH, 'model.bngl'), shared.parameter_overrides)
