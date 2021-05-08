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

from geometry import *

# create main model object
model = m.Model()

model.add_geometry_object(Cube)

# ---- initialization and execution ----

model.initialize()

for i in range(len(Cube.wall_list)):
    c = model.get_wall_color(Cube, i)
    
    if i in [3, 9]:
        assert c == color_green
    elif i in [1, 7]:
        assert c == color_red
    else:
        assert c == color_default

color_blue = m.Color(0, 0, 1, 0.4)
model.set_wall_color(Cube, 6, color_blue)

assert model.get_wall_color(Cube, 6) == color_blue

model.end_simulation()
