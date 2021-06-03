# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *

# ---- subsystem ----

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

sm = m.Species(
    name = 'sm',
    diffusion_constant_2d = 1e-7
)


# ---- create subsystem object and add components ----

subsystem = m.Subsystem()
subsystem.add_species(sm)
