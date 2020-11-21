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


subsystem = m.Subsystem()
model = m.Model()

d = m.ComponentType('d', ['X', 'Y'])
e = m.ComponentType('e', ['0', '1'])

for o,c in [(subsystem,'s'), (model,'m')]:
    mt1 = m.ElementaryMoleculeType('A' + c, [e,d], diffusion_constant_3d=1e-6)
    o.add_elementary_molecule_type(mt1)
    
    # must give a warning
    mt2 = m.ElementaryMoleculeType('A' + c, [d,e], diffusion_constant_3d=1e-6)
    o.add_elementary_molecule_type(mt2)
    assert len(o.elementary_molecule_types) == 1
        
    try:
        o.add_elementary_molecule_type(
            m.ElementaryMoleculeType('A' + c, [e,d], diffusion_constant_3d=1e-5))
        assert False
    except ValueError as err:
        print(err)

    assert len(o.elementary_molecule_types) == 1
