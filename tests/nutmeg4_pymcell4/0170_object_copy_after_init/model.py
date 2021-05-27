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


s = m.Species('A', diffusion_constant_3d = 1e-6)

s_before = copy.copy(s)

model = m.Model()
model.add_species(s)

model.initialize()

# this is allowed
s_before2 = copy.copy(s_before)

# this is not allowed - other fields may have been set and they are not copied yet
s_after = copy.copy(s)  # test checks this specific line


