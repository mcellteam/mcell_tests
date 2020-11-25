import mcell as m

from parameters import *

# ---- subsystem ----

a = m.Species(
    name = 'a',
    diffusion_constant_3d = 9.99999999999999955e-07
)

subsystem = m.Subsystem()
subsystem.add_species(a)
