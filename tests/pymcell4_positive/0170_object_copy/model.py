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

c2 = copy.copy(c)
c2.red = 0.5

# check that the original object is correct
assert c.red == 1
assert c2.red == 0.5

# object
rs = m.ReleaseSite(
    name = 'test',
    complex = m.Complex('A'),
    shape = m.Shape.SPHERICAL,
    location = (1, 2, 3),
    number_to_release = 1000
)

rs2 = copy.copy(rs)
rs2.complex = m.Complex('B')

assert rs.complex.to_bngl_str() == 'A'
assert rs2.complex.to_bngl_str() == 'B'

# vector
ct = m.ComponentType('u', states = ['0'])

ct2 = copy.copy(ct)
ct2.states = ['X', 'Y']

assert ct.states == ['0']
assert ct2.states == ['X', 'Y']  

# vector2
ct3 = m.ComponentType('u', states = ['0', '1'])

ct4 = copy.copy(ct3)
ct4.states[0] = 'X'

assert ct3.states == ['0', '1']
assert ct4.states == ['X', '1']  


# object that has all defaults set but requires 
#to be set to pass sematic check
cnt = m.Count(species_pattern = m.Complex('Z'), file_name = 'x')
cnt2 = copy.copy(cnt)




# checking that we are not doing deep copy
rs = m.ReleaseSite(
    name = 'test',
    complex = m.Complex('A'),
    shape = m.Shape.SPHERICAL,
    location = (1, 2, 3),
    number_to_release = 1000
)

rs2 = copy.copy(rs)
rs2.complex.name = 'B'

# both variants must stay the same
assert rs.complex.name == 'B'
assert rs2.complex.name == 'B' 

