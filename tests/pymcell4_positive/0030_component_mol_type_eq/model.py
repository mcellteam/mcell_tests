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

a1 = m.ComponentType('C', ['0', '1', 'Z'])
a2 = m.ComponentType('C', ['0', 'Z', '1'])
assert a1 == a2

b1 = m.ComponentType('C', ['0', '1', 'Z'])
b2 = m.ComponentType('D', ['0', 'Z', '1'])
assert b1 != b2

c1 = m.ComponentType('C', ['0', '1', 'Z'])
c2 = m.ComponentType('C', ['A', 'Z', '1'])
assert c1 != c2

# ComponentInstance
i1 = a1.inst('0')
i2 = a2.inst(0)
assert i1 == i2

j1 = a1.inst('0')
j2 = a2.inst('Z')
assert j1 != j2

k1 = a1.inst('0', 1)
k2 = a2.inst('0', 1)
assert k1 == k2

l1 = a1.inst('0', 1)
l2 = a2.inst('0', 2)
assert l1 != l2

m1 = b1.inst('0')
m2 = b2.inst('0')
assert m1 != m2

n1 = m.ElementaryMoleculeType('M', [b1, b2])
n2 = m.ElementaryMoleculeType('M', [b2, b1])
assert n1 == n2

c3 = m.ComponentType('E')
o1 = m.ElementaryMoleculeType('M', [b1, b2])
o2 = m.ElementaryMoleculeType('M', [b2, b1, c3])
assert o1 != o2

p1 = m.ElementaryMoleculeType('M')
p2 = m.ElementaryMoleculeType('N')
assert p1 != p2

zd = m.ComponentType('d', ['X', 'Y'])
ze = m.ComponentType('e', ['0', '1'])

zmt1 = m.ElementaryMoleculeType('A', [ze,zd], diffusion_constant_3d=1e-6)
zmt2 = m.ElementaryMoleculeType('A', [zd,ze], diffusion_constant_3d=1e-6)
assert zmt1 == zmt2

# ordering of component instances doesn't matter
q1 = n1.inst([b1.inst(0), b2.inst('Z')])
q2 = n1.inst([b2.inst('Z'), b1.inst(0)])
assert q1 == q2

r1 = n1.inst([b1.inst(1), b2.inst('Z')])
r2 = n1.inst([b2.inst('Z'), b1.inst(0)])
assert r1 != r2

# n1 and n2 are identical
s1 = n1.inst([b1.inst(0), b2.inst('Z')])
s2 = n2.inst([b2.inst('Z'), b1.inst(0)])
assert s1 == s2

t1 = n1.inst([b1.inst(0), b2.inst('Z')])
t2 = p2.inst()
assert t1 != t2
