#!/usr/bin/env python3

# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import sys
import os

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

import mcell as m

# ---- model parameters ----

# load parameters from BNGL
params = m.bngl_utils.load_bngl_parameters('model.bngl')

# ---- simulation setup ----

ITERATIONS = 1
TIME_STEP = 1e-06
DUMP = False
EXPORT_DATA_MODEL = True
SEED = 1


# create main model object
model = m.Model()

model.load_bngl('model.bngl')


# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS

model.notifications.rxn_and_species_report = False

model.config.partition_dimension = 2
model.config.subpartition_dimension = 0.2

model.initialize()


model.run_iterations(1)

num_VS = params['num_VS']
num_VCP = params['num_VCP']
num_VEC = params['num_VEC']
        
ids_VSCP = model.get_molecule_ids(pattern = m.Complex('@CP:V(s!1).S(v!1)'))
ids_VSPM = model.get_molecule_ids(pattern = m.Complex('@PM:V(s!1).S(v!1)'))
ids_VSEC = model.get_molecule_ids(pattern = m.Complex('@EC:V(s!1).S(v!1)'))

ids_VCP = model.get_molecule_ids(pattern = m.Complex('@CP:V'))
ids_VPM = model.get_molecule_ids(pattern = m.Complex('@PM:V'))
ids_VEC = model.get_molecule_ids(pattern = m.Complex('@EC:V'))


assert len(ids_VSCP) == 0
assert len(ids_VSPM) == num_VS
assert len(ids_VSEC) == 0

assert len(ids_VCP) == num_VCP
assert len(ids_VPM) == num_VS
assert len(ids_VEC) == num_VEC
            
model.end_simulation()
