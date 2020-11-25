import mcell as m

from parameters import *

# ---- subsystem ----

b = m.Species(
    name = 'b',
    diffusion_constant_2d = 5.00000000000000024e-05
)

a = m.Species(
    name = 'a',
    diffusion_constant_3d = 9.99999999999999955e-07
)

c = m.Species(
    name = 'c',
    diffusion_constant_3d = 9.99999999999999955e-07
)

react_a_and_b = m.ReactionRule(
    name = 'react_a_and_b',
    reactants = [ a.inst(orientation = m.Orientation.DOWN), b.inst(orientation = m.Orientation.UP) ],
    products = [ ],
    fwd_rate = 1e+08
)

subsystem = m.Subsystem()
subsystem.add_species(b)
subsystem.add_species(a)
subsystem.add_species(c)
subsystem.add_reaction_rule(react_a_and_b)
