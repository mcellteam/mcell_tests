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
assert len(ct_u.states) == 1
ct_u.states.append('1')
assert len(ct_u.states) == 2

ct_u.states[1] = '2'
assert ct_u.states[1] == '2' 
