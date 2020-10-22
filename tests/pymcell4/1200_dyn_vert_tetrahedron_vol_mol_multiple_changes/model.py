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

from parameters import *

if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])

import subsystem
import instantiation
import observables

model = m.Model()

# ---- configuration ----

model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations_hint = ITERATIONS

model.config.partition_dimension = 10
model.config.subpartition_dimension = 2.5

# ---- default configuration overrides ----

model.config.vacancy_search_distance = 0.1

# ---- add components ----

model.add_subsystem(subsystem.subsystem)
model.add_instantiation_data(instantiation.instantiation)
model.add_observables(observables.observables)

# ---- initialization and execution ----

model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    model.export_data_model()

tetrahedron_object = model.find_geometry_object('Tetrahedron')
assert tetrahedron_object

for i in range(ITERATIONS + 1):

    # mcell3 does geometry change as the first thing in an iteration 
    if i == 10:
        # even with this small change, some molecules are placed to a different wall than 
        # what moved it in mcell3
        model.add_vertex_move(tetrahedron_object, 0, m.Vec3(0, 0, -0.01))
        model.apply_vertex_moves()
        
    if i == 20:
        model.add_vertex_move(tetrahedron_object, 0, m.Vec3(0.01, 0.01, 0.01))
        model.apply_vertex_moves()        

    if i == 30:
        model.add_vertex_move(tetrahedron_object, 0, m.Vec3(0, 0, -0.01))
        model.add_vertex_move(tetrahedron_object, 1, m.Vec3(-0.01, 0, 0))
        model.add_vertex_move(tetrahedron_object, 2, m.Vec3(0, -0.01, 0))
        model.add_vertex_move(tetrahedron_object, 3, m.Vec3(0, +0.01, 0))
        model.apply_vertex_moves()        

    if i == 40:
        model.add_vertex_move(tetrahedron_object, 0, m.Vec3(0, 0, +0.01))
        model.add_vertex_move(tetrahedron_object, 1, m.Vec3(-0.005, 0, 0))
        #model.add_vertex_move(tetrahedron_object, 2, m.Vec3(0, -0.01, 0))
        model.add_vertex_move(tetrahedron_object, 3, m.Vec3(0, 0, -0.01))
        model.apply_vertex_moves()       
        
    model.run_iterations(1)

model.end_simulation()
