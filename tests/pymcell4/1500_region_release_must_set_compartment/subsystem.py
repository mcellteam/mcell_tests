# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

from parameters import *


Syk_a = m.ComponentType(
    name = 'a',
    states = ['Y', 'pY']
)

Syk_l = m.ComponentType(
    name = 'l',
    states = ['Y', 'pY']
)

Syk_tSH2 = m.ComponentType(
    name = 'tSH2'
)

Syk = m.ElementaryMoleculeType(
    name = 'Syk',
    components = [Syk_a, Syk_l, Syk_tSH2],
    diffusion_constant_3d = 8.50999999999999984e-07
)

# ---- create subsystem object and add components ----

subsystem = m.Subsystem()
subsystem.add_elementary_molecule_type(Syk)
