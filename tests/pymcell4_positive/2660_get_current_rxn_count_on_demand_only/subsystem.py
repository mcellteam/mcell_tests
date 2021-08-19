import mcell as m

from parameters import *
from bngl_molecule_types_info import *

# ---- subsystem ----

transp = m.SurfaceClass(
    name = 'transp',
    type = m.SurfacePropertyType.TRANSPARENT,
    affected_complex_pattern = m.AllMolecules
)

subsystem = m.Subsystem()
subsystem.add_surface_class(transp)

# load subsystem information from bngl file
subsystem.load_bngl_molecule_types_and_reaction_rules('model.bngl')
# set additional information such as diffusion constants for loaded elementary molecule types
set_bngl_molecule_types_info(subsystem)
