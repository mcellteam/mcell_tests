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

#em_a = subsystem.find_elementary_molecule_type('A')
#em_a.custom_time_step = 0.4e-6 # in us

#em_a = subsystem.find_elementary_molecule_type('R')
#em_a.custom_time_step = 0.4e-6 # in us

