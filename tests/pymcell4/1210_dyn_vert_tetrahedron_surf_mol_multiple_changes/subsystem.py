import mcell as m

from parameters import *

# ---- subsystem ----

sm = m.Species(
    name = 'sm',
    diffusion_constant_2d = 1e-7
)

subsystem = m.Subsystem()
subsystem.add_species(sm)
