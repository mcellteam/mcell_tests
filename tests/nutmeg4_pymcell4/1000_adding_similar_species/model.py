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


subsystem = m.Subsystem()
model = m.Model()

for o,c in [(subsystem,'s'), (model,'m')]:
    o.add_species(m.Species('A'+c, diffusion_constant_3d=1e-6))
    
    # should give a warning
    o.add_species(m.Species('A'+c, diffusion_constant_3d=1e-6))

    try:
        o.add_species(m.Species('A'+c, diffusion_constant_3d=1e-7))
        assert False
    except ValueError as err:
        print(err)

    # just declarations, expecting that the elementary molecule type  
    # will be defined before initialization
    o.add_species(m.Species('B'+c+'(a,b)'))
    
    # should not give a warning (not checked) 
    o.add_species(m.Species('B'+c+'(b,a)'))
