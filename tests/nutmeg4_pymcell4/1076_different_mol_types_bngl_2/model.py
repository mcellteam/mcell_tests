#!/usr/bin/env python3

# based on pymcell4_positive/2030_rule_eq

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m


# must not print a warning
s1 = m.Subsystem()
s1.load_bngl_molecule_types_and_reaction_rules('test1.bngl')
    
# must not cause an error
s2 = m.Subsystem()
s2.load_bngl_molecule_types_and_reaction_rules('test2.bngl')


model = m.Model()
model.add_subsystem(s1)
model.add_subsystem(s2)

model.initialize()


