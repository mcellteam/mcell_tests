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
    # just declarations, expecting that the elementary molecule type  
    # will be defined before initialization
    o.add_species(m.Species('B'+c+'(a,b)'))
    
    # should not give a warning (not checked),
    # we do not care about adding declarations, after initialization they will be 
    # ignored 
    o.add_species(m.Species('B'+c+'(b,a)'))

# also check that initialization fails
# because we don't know the diffusion constant 
try:
    model.initialize()
    assert False
except ValueError as err:
    assert "was set" in str(err)
