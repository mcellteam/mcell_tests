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

a1 = m.Complex('a')
a2 = m.Complex('a')
assert a1 == a2 

# check that cached canonical name is updated
a2.name = 'b'
assert a1 != a2 

b1 = m.Complex('a')
b2 = m.Complex('b')
assert b1 != b2 

b2.name = 'a'
assert b1 == b2 

c1 = m.Complex('A(b!1).B(a!1)')
c2 = m.Complex('B(a!1).A(b!1)')
assert c1 == c2 

d1 = m.Complex('@C1:A(b!1).B(a!1)')
d2 = m.Complex('@C2:B(a!1).A(b!1)')
assert d1 != d2 

e1 = m.Complex('A(b!+)')
e2 = m.Complex('A(b!+)')
assert e1 == e2 

f1 = m.Complex('A(b!+)')
f2 = m.Complex('A(b!?)')
assert f1 != f2 

g1 = m.Complex('A(b!1).B(a!1)')
g2 = m.Complex('B(a!2).A(b!2)')
assert g1 == g2 

h1 = m.Complex('A(b)', orientation = m.Orientation.UP)
h2 = m.Complex('A(b)', orientation = m.Orientation.DOWN)
assert h1 != h2 
