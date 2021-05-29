import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m


model = m.Model()

rep = str(model)

# check that these classes are printed out
assert 'Config' in rep
assert 'Warnings' in rep
assert 'Notifications' in rep
