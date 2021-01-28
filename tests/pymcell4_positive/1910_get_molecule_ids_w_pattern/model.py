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

num_AR = params['num_AR']
num_AS = params['num_AS']
num_BT = params['num_BT']
num_BU = params['num_BU']
num_ASBT = params['num_ASBT']
num_ARBU = params['num_ARBU']
        
ids_A = model.get_molecule_ids(pattern = m.Complex('A'))
ids_B = model.get_molecule_ids(pattern = m.Complex('B'))
ids_AR = model.get_molecule_ids(pattern = m.Complex('A(a~R)'))
ids_AS = model.get_molecule_ids(pattern = m.Complex('A(a~S)'))
ids_BT = model.get_molecule_ids(pattern = m.Complex('B(b~T)'))
ids_BU = model.get_molecule_ids(pattern = m.Complex('B(b~U)'))

ids_ASBT = model.get_molecule_ids(pattern = m.Complex('A(a~S,b!1).B(b~T,a!1)'))
ids_ARBU = model.get_molecule_ids(pattern = m.Complex('A(a~R,b!1).B(b~U,a!1)'))

ids_AB = model.get_molecule_ids(pattern = m.Complex('A(b!1).B(a!1)'))

assert len(ids_A) == num_AR + num_AS + num_ASBT + num_ARBU
assert len(ids_B) == num_BT + num_BU + num_ASBT + num_ARBU
assert len(ids_AR) == num_AR + num_ARBU
assert len(ids_AS) == num_AS + num_ASBT
assert len(ids_BT) == num_BT + num_ASBT
assert len(ids_BU) == num_BU + num_ARBU
assert len(ids_ASBT) == num_ASBT
assert len(ids_ARBU) == num_ARBU
assert len(ids_AB) == num_ASBT + num_ARBU
            
model.end_simulation()
