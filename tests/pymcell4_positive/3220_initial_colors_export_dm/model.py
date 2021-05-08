#!/usr/bin/env python3

import sys
import os
import json

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

import geometry

# create main model object
model = m.Model()

model.add_geometry_object(geometry.Cube)
print(geometry.Cube)

# ---- initialization and execution ----

model.initialize()


model.export_data_model('out.json')

model.end_simulation()

# check JSON
with open('out.json', 'r') as fin:
    dm = json.load(fin)
    cube_dm = dm["mcell"]["geometrical_objects"]["object_list"][0]
    assert len(cube_dm["material_names"]) == 3
    assert cube_dm["element_material_indices"] == [0, 1, 0, 2, 0, 0, 0, 1, 0, 2, 0, 0]
    
    mats = dm["mcell"]["materials"]["material_dict"]
    assert "color_00ff003f" in mats