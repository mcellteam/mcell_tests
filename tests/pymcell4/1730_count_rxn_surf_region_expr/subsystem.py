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
subsystem.load_bngl_molecule_types_and_reaction_rules('test.bngl')
