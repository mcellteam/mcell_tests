import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m


# checking that .append and other modifications works
ct_u = m.ComponentType('u', states = ['0'])

#print(type(ct_u.states))
assert len(ct_u.states) == 1
ct_u.states.append('1')
assert len(ct_u.states) == 2

ct_u.states[1] = '2'
assert ct_u.states[1] == '2' 


rs = m.ReleaseSite(
    name = 'test',
    complex = m.Complex('A'),
    shape = m.Shape.SPHERICAL,
    location = (1, 2, 3),
    number_to_release = 1000
)

#print(type(rs.location))
#print(rs.location)
rs.location[0] = 2
#print(rs.location)
assert rs.location[0] == 2