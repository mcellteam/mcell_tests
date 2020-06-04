#!/usr/bin/env python3

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

r2 = m.ReactionRule('r', [a.inst()], [], 0)
model.add_reaction_rule(r2)
 