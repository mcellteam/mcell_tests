#!/usr/bin/env python3

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

c1_1 = m.ComponentType('C', ['0', '1', 'Z'])
c1_2 = m.ComponentType('C', ['1', '0', 'Z'])
b1 = m.ComponentType('B', ['0', '1', 'Q'])

mt1_1 = m.ElementaryMoleculeType('M', [c1_1, b1], diffusion_constant_3d=1e-6)
mt2   = m.ElementaryMoleculeType('M', [b1, c1_2], diffusion_constant_3d=1e-5)

# different diffusion constant of used mol type
s5_1 = m.Species(elementary_molecule_instances = [mt1_1.inst([c1_1.inst('0'), b1.inst('Q')])])
s5_2 = m.Species(elementary_molecule_instances = [mt2.inst([c1_1.inst('0'), b1.inst('Q')])])
assert s5_1 != s5_2
