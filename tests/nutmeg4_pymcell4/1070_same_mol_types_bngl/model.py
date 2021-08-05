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
model = m.Model()
model.load_bngl_molecule_types_and_reaction_rules('test1.bngl')
model.load_bngl_molecule_types_and_reaction_rules('test2.bngl')

model.initialize()

print("Passed")
