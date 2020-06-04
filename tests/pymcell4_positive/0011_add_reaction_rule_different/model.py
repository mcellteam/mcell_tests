#!/usr/bin/env python3

# based on mcell_tests/tests/mdl/0320_2_mols_react_in_box_it_10
# rewritten to look like a generated file 

import sys
import os

MCELL_DIR = os.environ.get('MCELL_DIR', '')
if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'lib'))
else:
    print("Error: variable MCELL_DIR that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

model = m.Model()

a = m.Species('a', diffusion_constant_3d = 1e-6)

r = m.ReactionRule('r', [a.inst()], [], 0)
model.add_reaction_rule(r)

b = m.Species('b', diffusion_constant_3d = 1e-6)

r2 = m.ReactionRule('r', [b.inst()], [], 0)

try:
    model.add_reaction_rule(r2) # muth throw exc
    assert False
except ValueError: 
    pass # ok
 