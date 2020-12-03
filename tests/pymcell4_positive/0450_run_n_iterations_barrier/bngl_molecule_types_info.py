import mcell as m

from parameters import *

# set additional information about species and molecule types that cannot be stored in BNGL,
# elementary molecule types are already in the subsystem or model after they were loaded from BNGL
def set_bngl_molecule_types_info(subsystem):
    b = subsystem.find_elementary_molecule_type('b')
    assert b, "Elementary molecule type 'b' was not found"
    b.diffusion_constant_3d = 9.99999999999999955e-07

    a = subsystem.find_elementary_molecule_type('a')
    assert a, "Elementary molecule type 'a' was not found"
    a.diffusion_constant_3d = 9.99999999999999955e-08
    a.custom_space_step = 0.10000000000000001
    a.target_only = True

    c = subsystem.find_elementary_molecule_type('c')
    assert c, "Elementary molecule type 'c' was not found"
    c.diffusion_constant_3d = 9.99999999999999955e-08
    c.custom_space_step = 0.10000000000000001
    c.target_only = True


