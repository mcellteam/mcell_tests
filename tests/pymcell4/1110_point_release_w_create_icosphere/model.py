#!/usr/bin/env python3

# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import sys
import os
import importlib.util

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

# ---- import mcell module located in directory ----
# ---- specified by system variable MCELL_PATH  ----
MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, 'lib')
    if os.path.exists(os.path.join(lib_path, 'mcell.so')) or \
        os.path.exists(os.path.join(lib_path, 'mcell.pyd')):
        sys.path.append(lib_path)
    else:
        print("Error: Python module mcell.so or mcell.pyd was not found in "
              "directory '" + lib_path + "' constructed from system variable "
              "MCELL_PATH.")
        sys.exit(1)
else:
    print("Error: system variable MCELL_PATH that is used to find the mcell "
          "library was not set.")
    sys.exit(1)

import mcell as m

# parameters are intentionally not imported using from ... import *
# because we may need to make changes to the module's variables
import parameters

# create main model object
model = m.Model()

a = m.Species(
    name = 'a',
    diffusion_constant_3d = 9.99999999999999955e-07
)

# ---- create subsystem object and add components ----

model.add_species(a)


rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = a.inst(),
    # shape = m.Shape.SPHERICAL, # - must work even without this specification
    location = (0, 0, 0),
    site_diameter = 0,
    number_to_release = 2
)


model.add_release_site(rel_a)


sphere = m.geometry_utils.create_icosphere('sphere', 0.1, 3)
model.add_geometry_object(sphere)


viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(parameters.SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)
model.add_viz_output(viz_output)

# ---- configuration ----

model.config.time_step = parameters.TIME_STEP
model.config.seed = parameters.SEED
model.config.total_iterations = parameters.ITERATIONS

model.notifications.rxn_and_species_report = True

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- default configuration overrides ----

# ---- add components ----

model.initialize()

if parameters.DUMP:
    model.dump_internal_state()

if parameters.EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

model.run_iterations(parameters.ITERATIONS)
model.end_simulation()
