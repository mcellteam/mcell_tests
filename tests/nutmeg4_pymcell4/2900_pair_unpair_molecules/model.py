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
    diffusion_constant_2d = 1e-8
)
model.add_species(a)

b = m.Species(
    name = 'b',
    diffusion_constant_2d = 1e-8
)
model.add_species(b)

v = m.Species(
    name = 'v',
    diffusion_constant_3d = 1e-8
)
model.add_species(v)

box1 = m.geometry_utils.create_box('box1', 0.2)
model.add_geometry_object(box1)

box2 = m.geometry_utils.create_box('box2', 0.2)
box2.translate((0.5, 0, 0))
model.add_geometry_object(box2)

rel_a = m.ReleaseSite(
    name = 'rel_a',
    complex = a,
    region = box1,
    number_to_release = 10
)
model.add_release_site(rel_a)

rel_b = m.ReleaseSite(
    name = 'rel_b',
    complex = b,
    region = box2,
    number_to_release = 10
)
model.add_release_site(rel_b)


rel_v = m.ReleaseSite(
    name = 'rel_v',
    complex = v,
    region = box2,
    number_to_release = 10
)
model.add_release_site(rel_v)

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

model.notifications.rxn_and_species_report = False

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.5

# ---- default configuration overrides ----

# ---- add components ----

model.initialize()

if parameters.DUMP:
    model.dump_internal_state()

if parameters.EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

# release molecules
model.run_iterations(1)

ida = 0
idb = 10
idv = 20

# check species
ma = model.get_molecule(ida)
assert model.get_species_name(ma.species_id) == 'a'
mb = model.get_molecule(idb)
assert model.get_species_name(mb.species_id) == 'b'
mv = model.get_molecule(idv)
assert model.get_species_name(mv.species_id) == 'v'

# tests

# pair correct
model.pair_molecules(ida, idb)

# unpair correct
model.unpair_molecules(ida, idb)

# pair paired
model.pair_molecules(ida, idb)

try:
    model.pair_molecules(ida, 11)
except RuntimeError as e:
    print(e)

# pair volume mol
try:
    model.pair_molecules(idv, 11)
except RuntimeError as e:
    print(e)

# pair same object
try:
    model.pair_molecules(1, 2)
except RuntimeError as e:
    print(e)

# unpair unpaired 
try:
    model.unpair_molecules(1, 11)
except RuntimeError as e:
    print(e)

# invalid molecule
try:
    model.pair_molecules(5, 100)
except RuntimeError as e:
    print(e)

try:
    model.pair_molecules(100, 5)
except RuntimeError as e:
    print(e)


model.unpair_molecules(ida, idb)

# pair correct
model.pair_molecules(ida, idb)
# pair correct
model.pair_molecules(ida + 1, idb + 2)

# get_paired_molecule correct
assert model.get_paired_molecule(ida) == idb
assert model.get_paired_molecule(ida + 1) == idb + 2  

# get_paired_molecule unexpected
assert model.get_paired_molecule(ida + 2) == m.ID_INVALID  

model.end_simulation()
