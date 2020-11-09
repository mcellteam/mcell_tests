import mcell as m

from parameters import *
from bngl_molecule_types_info import *

# ---- subsystem ----

cclamp_left = m.SurfaceClass(
    name = 'cclamp_left',
    type = m.SurfacePropertyType.CONCENTRATION_CLAMP,
    affected_complex_pattern = m.Complex('a', orientation = m.Orientation.DOWN), # DOWN means towards the center of the object 
    concentration = 1e-5
)

cclamp_right = m.SurfaceClass(
    name = 'cclamp_right',
    type = m.SurfacePropertyType.CONCENTRATION_CLAMP,
    affected_complex_pattern = m.Complex('a', orientation = m.Orientation.DOWN),
    concentration = 1e-7
)

subsystem = m.Subsystem()
subsystem.add_surface_class(cclamp_left)
subsystem.add_surface_class(cclamp_right)

# load subsystem information from bngl file
subsystem.load_bngl_molecule_types_and_reaction_rules('model.bngl')
# set additional information such as diffusion constants for loaded elementary molecule types
set_bngl_molecule_types_info(subsystem)
