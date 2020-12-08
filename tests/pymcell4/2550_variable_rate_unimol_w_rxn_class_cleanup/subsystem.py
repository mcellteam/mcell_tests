import mcell as m

from parameters import *

# ---- subsystem ----

b = m.Species(
    name = 'b',
    diffusion_constant_3d = 4.99999999999999977e-07
)

a = m.Species(
    name = 'a',
    diffusion_constant_3d = 9.99999999999999955e-07
)


react_a_to_b = m.ReactionRule(
    name = 'react_a_to_b',
    reactants = [ a.inst() ],
    products = [ b.inst() ],
    variable_rate = var_rate_react_a_to_b_1
)

subsystem = m.Subsystem()
subsystem.add_species(b)
subsystem.add_species(a)
subsystem.add_reaction_rule(react_a_to_b)
