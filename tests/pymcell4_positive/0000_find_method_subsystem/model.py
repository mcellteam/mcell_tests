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

model = m.Model()

a = m.Species('a', diffusion_constant_3d = 1e-6)
model.add_species(a)
s1 = model.find_species('a')
assert s1 is not None and s1.name == 'a'
s2 = model.find_species('b')
assert s2 is None 

r = m.ReactionRule('r', [a.inst()], [], 0)
model.add_reaction_rule(r)
r1 = model.find_reaction_rule('r')
assert r1 is not None and r1.name == 'r'
r2 = model.find_reaction_rule('s')
assert r2 is None 

sc = m.SurfaceClass('sc', type = m.SurfacePropertyType.TRANSPARENT, affected_complex_pattern = a)
model.add_surface_class(sc)
sc1 = model.find_surface_class('sc')
assert sc1 is not None and sc1.name == 'sc'
sc2 = model.find_surface_class('scx')
assert sc2 is None
 