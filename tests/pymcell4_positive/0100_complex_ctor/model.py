#!/usr/bin/env python3

# test to check that the Complex constructor correctly initializes internal 
# representation

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

c = m.Complex('@C1:A(b~X!1).B(a!1)')
#print(c)

assert len(c.elementary_molecules) == 2

em0 = c.elementary_molecules[0]
em1 = c.elementary_molecules[1]
assert len(em0.components) == 1
assert len(em1.components) == 1

assert em0.elementary_molecule_type.name == 'A'

comp0 = em0.components[0]
assert comp0.bond == 1
assert comp0.state == 'X'

comp_type0 = comp0.component_type
assert comp_type0.name == 'b'

assert c.orientation == m.Orientation.DEFAULT
assert c.elementary_molecules[0].compartment_name == 'C1'
assert c.elementary_molecules[1].compartment_name == 'C1'
