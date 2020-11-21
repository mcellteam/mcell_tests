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
mt1_2 = m.ElementaryMoleculeType('M', [b1, c1_2])
mt2   = m.ElementaryMoleculeType('M', [b1, c1_2], diffusion_constant_3d=1e-5)

mt4 = m.ElementaryMoleculeType('N', [b1, b1, c1_1])
mt5 = m.ElementaryMoleculeType('O', [b1, c1_2])

s1_1 = m.Species(elementary_molecule_instances = [mt1_1.inst([c1_1.inst('0'), b1.inst('Q')])])
s1_2 = m.Species(elementary_molecule_instances = [mt1_1.inst([b1.inst('Q'), c1_1.inst('0')])])
assert s1_1 == s1_2

s1_3 = m.Species(elementary_molecule_instances = [mt1_2.inst([b1.inst('Q'), c1_2.inst('0')])])
assert s1_1 == s1_3


s2_1 = m.Species(elementary_molecule_instances = 
                [
                    mt1_1.inst([c1_1.inst('0'), b1.inst('Q', bond=1)]), 
                    mt4.inst([b1.inst('0'), b1.inst('Q', bond=1), c1_1.inst('0')])
                ]
)
s2_2 = m.Species(elementary_molecule_instances = 
                [
                    mt4.inst([b1.inst('0'), b1.inst('Q', bond=1), c1_1.inst('0')]),
                    mt1_2.inst([c1_1.inst('0'), b1.inst('Q', bond=1)]) 
                ]
)
assert s2_1 == s2_2

# different bonds
s3 = m.Species(elementary_molecule_instances = 
                [
                    mt4.inst([b1.inst('0'), b1.inst('Q', bond=1), c1_1.inst('0')]),
                    mt1_2.inst([c1_1.inst('0', bond=1), b1.inst('Q')]) 
                ]
)
assert s2_1 != s3

# different state
s4 = m.Species(elementary_molecule_instances = 
                [
                    mt4.inst([b1.inst('Q'), b1.inst('Q', bond=1), c1_1.inst('0')]),
                    mt1_2.inst([c1_1.inst('0', bond=1), b1.inst('Q')]) 
                ]
)
assert s2_1 != s4
