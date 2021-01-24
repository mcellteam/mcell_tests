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

import parameters

if len(sys.argv) == 1:
    # no arguments
    pass
elif len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value of seed defined in module parameters
    parameters.SEED = int(sys.argv[2])
else:
    print("Error: invalid command line arguments")
    print("  usage: " + sys.argv[0] + "[-seed N]")
    sys.exit(1)


# create main model object
model = m.Model()

model.load_bngl('model.bngl', './react_data/seed_' + str(parameters.SEED).zfill(5) + '/')

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
model.config.subpartition_dimension = 0.2

model.initialize()

if parameters.DUMP:
    model.dump_internal_state()

if parameters.EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()



model.run_iterations(1)
        
all_ids = model.get_molecule_ids()
assert len(all_ids) == 2 
        
        
def check_eq(v1, v2):
    EPS = 1e-6
    assert abs(v1.x - v2.x) < EPS
    assert abs(v1.y - v2.y) < EPS
    assert abs(v1.z - v2.z) < EPS 

def check_eq2(v1, v2):
    EPS = 1e-6
    assert abs(v1.x - v2.x) < EPS
    assert abs(v1.y - v2.y) < EPS
            
va = model.get_molecule(all_ids[0])
#print(va)
assert va.type == m.MoleculeType.VOLUME
check_eq(va.pos3d, m.Vec3(0.057759, 0.0187056, 0.0920891))
assert va.species_id == 3 # may change in the future 
assert va.orientation == m.Orientation.NONE
assert not va.geometry_object
assert va.wall_index == -1

sb = model.get_molecule(all_ids[1])        
#print(sb)
assert sb.type == m.MoleculeType.SURFACE
check_eq(sb.pos3d, m.Vec3(-0.0134432, 0.111673, 0.125))
check_eq2(sb.pos2d, m.Vec2(0.0883063, 0.0694588))
assert sb.species_id == 4 # may change in the future 
assert sb.orientation == m.Orientation.UP
assert sb.geometry_object is model.find_geometry_object('CP')
assert sb.wall_index == 5

    
model.end_simulation()
