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

# single property
rs1 = m.ReleaseSite(
    'rel1', 
    complex = m.Complex('X(y!1).Y(x!1)'),
    shape = m.Shape.SPHERICAL,
    location = m.Vec3(1),
    number_to_release = 10
)

rs2 = m.ReleaseSite(
    'rel1', 
    complex = m.Complex('X(y!1).Y(x!1)'),
    shape = m.Shape.SPHERICAL,
    location = m.Vec3(0.1),
    number_to_release = 10
)

i1 = m.InstantiationData()
i1.add_release_site(rs1)
# error
try:
    i1.add_release_site(rs2)
    assert False
except ValueError as err:
    print(err)
    
rs3 = m.ReleaseSite(
    'rel2', 
    complex = m.Complex('X(y!1).Y(x!1)'),
    shape = m.Shape.SPHERICAL,
    location = m.Vec3(1),
    number_to_release = 10
)

    
rs4 = m.ReleaseSite(
    'rel2', 
    complex = m.Complex('Y(x!1).X(y!1)'),
    shape = m.Shape.SPHERICAL,
    location = m.Vec3(1),
    number_to_release = 10
)

i2 = m.InstantiationData()
i2.add_release_site(rs3)
# warning
i2.add_release_site(rs4)

