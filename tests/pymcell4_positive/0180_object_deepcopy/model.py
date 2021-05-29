import sys
import os
import copy

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

# numerical attribute
c = m.Color(red = 1, green = 0, blue = 0, alpha = 1)

c2 = copy.deepcopy(c)
c2.red = 0.5

# check that the original object is correct
assert c.red == 1
assert c2.red == 0.5

# object - first level copy
rs = m.ReleaseSite(
    name = 'test',
    complex = m.Complex('A'),
    shape = m.Shape.SPHERICAL,
    location = (1, 2, 3),
    number_to_release = 1000
)

rs2 = copy.deepcopy(rs)
rs2.complex.name = 'B'

assert rs.complex.name == 'A'
assert rs2.complex.name == 'B' 

# object in vector
cplx = m.Complex('X(a~0!1).Y(b~Q!1)')

ct = m.ComponentType('z', ['E','R'])

cplx2 = copy.deepcopy(cplx)

cplx2.elementary_molecules[0].elementary_molecule_type.components[0] = ct
cplx2.elementary_molecules[0].components[0] = ct.inst('E', 1)

assert cplx.elementary_molecules[0].elementary_molecule_type.components[0].name == 'a'
assert cplx.to_bngl_str() == 'X(a~0!1).Y(b~Q!1)'
assert cplx2.to_bngl_str() == 'X(z~E!1).Y(b~Q!1)'


