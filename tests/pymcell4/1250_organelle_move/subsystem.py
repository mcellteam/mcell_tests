import mcell as m

from parameters import *
from bngl_molecule_types_info import *

# ---- subsystem ----

subsystem = m.Subsystem()

# load subsystem information from bngl file
subsystem.load_bngl_molecule_types_and_reaction_rules('model.bngl')
# set additional information such as diffusion constants for loaded elementary molecule types
set_bngl_molecule_types_info(subsystem)
