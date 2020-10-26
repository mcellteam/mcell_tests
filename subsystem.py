import mcell as m

from parameters import *

# ---- subsystem ----

A = m.Species(
    name = 'A',
    diffusion_constant_3d = 1e-6
)

Mem = m.Species(
    name = 'Mem',
    diffusion_constant_2d = 1e-8
)

B = m.Species(
    name = 'B',
    diffusion_constant_3d = 2e-6
)

reflect = m.SurfaceClass(
    name = 'reflect',
    type = m.SurfacePropertyType.REFLECTIVE,
    affected_species = m.AllMolecules
)

unnamed_reaction_rule_0 = m.ReactionRule(
    name = 'unnamed_reaction_rule_0',
    reactants = [ A.inst(compartment_name = 'CP') ],
    products = [ B.inst(compartment_name = 'CP') ],
    fwd_rate = 1e6
)

unnamed_reaction_rule_1 = m.ReactionRule(
    name = 'unnamed_reaction_rule_1',
    reactants = [ A.inst(compartment_name = 'EC'), Mem.inst(compartment_name = 'PM') ],
    products = [ A.inst(compartment_name = 'CP'), Mem.inst(compartment_name = 'PM') ],
    fwd_rate = 1e8
)

subsystem = m.Subsystem()
subsystem.add_species(A)
subsystem.add_species(Mem)
subsystem.add_species(B)
subsystem.add_surface_class(reflect)
subsystem.add_reaction_rule(unnamed_reaction_rule_0)
subsystem.add_reaction_rule(unnamed_reaction_rule_1)
