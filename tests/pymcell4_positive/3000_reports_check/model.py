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

ITERATIONS = int(params['ITERATIONS'])

# ---- load bngl file ----

model = m.Model()

if 'MCELL_DEFAULT_COMPARTMENT_VOLUME' in params:
    MCELL_DEFAULT_COMPARTMENT_VOLUME = params['MCELL_DEFAULT_COMPARTMENT_VOLUME']
    MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH = MCELL_DEFAULT_COMPARTMENT_VOLUME**(1.0/3.0) 
    default_compartment = m.geometry_utils.create_box(
        'default_compartment', MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH
    )
    model.add_geometry_object(default_compartment)
else:
    MCELL_DEFAULT_COMPARTMENT_EDGE_LENGTH = 1
    default_compartment = None

model.load_bngl('test.bngl', './react_data/seed_' + str(1).zfill(5) + '/', default_compartment)


# ---- configuration ----

model.config.total_iterations_hint = ITERATIONS 

model.notifications.rxn_and_species_report = True

model.initialize()
model.run_iterations(ITERATIONS)
model.end_simulation()

# check that reports exist
assert os.path.exists(os.path.join('reports', 'rxn_report_00001.txt'))
assert os.path.exists(os.path.join('reports', 'species_report_00001.txt'))
assert os.path.exists(os.path.join('reports', 'warnings_report_00001.txt'))

