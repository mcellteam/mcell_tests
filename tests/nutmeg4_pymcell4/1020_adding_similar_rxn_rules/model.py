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

s1 = m.Subsystem()
s1.load_bngl_molecule_types_and_reaction_rules('test1.bngl')

s2 = m.Subsystem()
s2.load_bngl_molecule_types_and_reaction_rules('test2.bngl')

model = m.Model()
model.add_subsystem(s1)

for o,c in [(s1,'s'), (model,'m')]:
    
    print(len(o.reaction_rules))
    assert len(o.reaction_rules) == 6
    
    # must print warning
    o.add_reaction_rule(s2.reaction_rules[0])
    print(len(o.reaction_rules))
    assert len(o.reaction_rules) == 6
    
    o.add_reaction_rule(s2.reaction_rules[1])
    o.add_reaction_rule(s2.reaction_rules[2])
    o.add_reaction_rule(s2.reaction_rules[3])
    o.add_reaction_rule(s2.reaction_rules[4])
    
    try:
        o.add_reaction_rule(s2.reaction_rules[5])
        assert False
    except ValueError as err:
        print(err)
        
    assert len(o.reaction_rules) == 7 # only Y(x) -> Null 456 is added
    
    
m2 = m.Model()
m2.add_subsystem(s1)
try:
    m2.add_subsystem(s2)
    assert False
except ValueError as err:
    print(err)   

assert len(m2.reaction_rules) == 7 # only Y(x) -> Null 456 is added
    