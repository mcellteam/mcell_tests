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
model.load_bngl('test.bngl', '')

assert model.counts[0].molecules_pattern.to_bngl_str() == 'X(y,p~0,p~0)'

assert model.reaction_rules[0].to_bngl_str() == 'X(y!1,p~0).Y(x!1) -> X(y,p~0) + Y(x)'
assert model.reaction_rules[1].to_bngl_str() == 'Y(x) -> Null'
