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


params = m.bngl_utils.load_bngl_parameters('test.bngl')


box1 = m.geometry_utils.create_box('box1', 0.5)
box2 = m.geometry_utils.create_box('box2', 1)
box3 = m.geometry_utils.create_box('box3', 1.5)

ct_box2 = m.CountTerm(
    species_pattern = m.Complex('A'),
    region = box2
)
ct_box1 = m.CountTerm(
    species_pattern = m.Complex('A'),
    region = box1
)

ct_box2_minus_ct_box1 = ct_box2 - ct_box1

# setting region that will be ignored
ct_box2_minus_ct_box1.region = box3

count = m.Count(
    name = 'z',
    expression = ct_box2_minus_ct_box1,
    file_name = 'x'    
)


# ---- load bngl file ----

# must be checked during initialization
model = m.Model()

model.load_bngl('test.bngl')

model.add_count(count)
model.add_geometry_object(box1)
model.add_geometry_object(box2)
model.add_geometry_object(box3)

model.initialize()

model.end_simulation()

