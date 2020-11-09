import mcell as m

from parameters import *

# set additional information about species and molecule types that cannot be stored in BNGL,
# elementary molecule types are already in the subsystem or model after they were loaded from BNGL
def set_bngl_molecule_types_info(subsystem):
    a = subsystem.find_elementary_molecule_type('a')
    assert a, "Elementary molecule type 'a' was not found"
    a.diffusion_constant_3d = 1e-6


