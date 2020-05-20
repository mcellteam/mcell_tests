import mcell as m

from parameters import *

# This generated file defines the following objects:
# a: m.Species
# b: m.Species
# c: m.Species
# react_a_and_b: m.ReactionRule
# subsystem: m.Subsystem

# ------- subsystem ---------

a = m.Species('a', diffusion_constant_3d = 1e-6)
b = m.Species('b', diffusion_constant_3d = 0.5e-6)
c = m.Species('c', diffusion_constant_3d = 1e-6)

react_a_and_b = m.ReactionRule(
    name = 'react_a_and_b',
    reactants = [ a.inst(), b.inst()],
    products = [ c.inst() ],
    fwd_rate = 5e8
)

subsystem = m.Subsystem()
subsystem.add_species(a)
subsystem.add_species(b)
subsystem.add_species(c)
subsystem.add_reaction_rule(react_a_and_b)
