import sys
import os


MCELL_DIR = os.environ.get('MCELL_DIR', '')
if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'lib'))
else:
    print("Error: variable MCELL_DIR that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

a = m.Vec3(1.5, 2.0, 3)
assert a.x == 1.5
assert a.y == 2.0
assert a.z == 3.0

b = m.Vec3(2.5, 1.0, 2)

assert a != b

c = a + b
assert c == m.Vec3(4.0, 3.0, 5.0)

a.z = 2.0
assert a.z == 2.0

d = a - b
assert d == m.Vec3(-1, 1, 0)

e = a * b
assert e == m.Vec3(1.5*2.5, 2*1, 2*2)

e = a / b
assert e == m.Vec3(1.5/2.5, 2/1, 2/2)



"""
disabled temporarily 

a = m.IVec3(5, 2, 3)
assert a.x == 5
assert a.y == 2
assert a.z == 3

b = m.IVec3(2, 1, 2)

assert a != b

c = a + b
assert c == m.IVec3(5+2, 2+1, 3+2)

a.z = 2
assert a.z == 2

d = a - b
assert d == m.IVec3(5-2, 2-1, 2-2)

e = a * b
assert e == m.IVec3(5*2, 2*1, 2*2)

e = a / b
assert e == m.IVec3(5/2, 2/1, 2/2)
"""