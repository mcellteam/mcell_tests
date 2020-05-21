import mcell as m

from parameters import *

# ---- subsystem ----

b = m.Species(
    name = 'b',
    diffusion_constant_3d = 4.9999999999999998e-07
)

a = m.Species(
    name = 'a',
    diffusion_constant_3d = 9.9999999999999995e-07
)

c = m.Species(
    name = 'c',
    diffusion_constant_3d = 9.9999999999999995e-07
)

react_a_and_b = m.ReactionRule(
    name = 'react_a_and_b',
    reactants = [ a.inst(), b.inst() ],
    products = [ c.inst() ],
    fwd_rate = 500000000
)

subsystem = m.Subsystem()
subsystem.add_species(b)
subsystem.add_species(a)
subsystem.add_species(c)
subsystem.add_reaction_rule(react_a_and_b)
