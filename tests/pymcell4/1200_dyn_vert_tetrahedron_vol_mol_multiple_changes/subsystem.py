import mcell as m

from parameters import *

# ---- subsystem ----

vm = m.Species(
    name = 'vm',
    diffusion_constant_3d = 1e-05
)

subsystem = m.Subsystem()
subsystem.add_species(vm)
