import mcell as m

from parameters import *

# set additional information about species and molecule types that cannot be stored in BNGL,
# elementary molecule types are already in the subsystem or model after they were loaded from BNGL
def set_bngl_molecule_types_info(subsystem):
    a = subsystem.find_elementary_molecule_type('a')
    assert a, "Elementary molecule type 'a' was not found"
    a.diffusion_constant_3d = 1e-6

    b = subsystem.find_elementary_molecule_type('b')
    assert b, "Elementary molecule type 'b' was not found"
    b.diffusion_constant_3d = 1e-6

    c = subsystem.find_elementary_molecule_type('c')
    assert c, "Elementary molecule type 'c' was not found"
    c.diffusion_constant_3d = 1e-6

    d = subsystem.find_elementary_molecule_type('d')
    assert d, "Elementary molecule type 'd' was not found"
    d.diffusion_constant_3d = 1e-6

    t1 = subsystem.find_elementary_molecule_type('t1')
    assert t1, "Elementary molecule type 't1' was not found"
    t1.diffusion_constant_2d = 1e-7

    t2 = subsystem.find_elementary_molecule_type('t2')
    assert t2, "Elementary molecule type 't2' was not found"
    t2.diffusion_constant_2d = 1e-8


