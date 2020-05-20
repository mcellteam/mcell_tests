#!/usr/bin/env python3

# based on mcell_tests/tests/mdl/0320_2_mols_react_in_box_it_10

import sys
import os

# TODO: can we somehow get rid of this? 
# install using pip
MCELL_DIR = os.environ.get('MCELL_DIR', '')

if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'lib'))
else:
    print("Error: variable MCELL_DIR that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

SEED = 1
ITERATIONS = 10

# ------- subsystem ---------

a = m.Species('a', diffusion_constant_3d = 1e-6)
b = m.Species('b', diffusion_constant_3d = 0.5e-6)
c = m.Species('c', diffusion_constant_3d = 1e-6)

react_a_and_b = m.ReactionRule(
    name = 'react_a_and_b',
    reactants = [ a.inst(), b.inst()],
    products = [ c.inst() ],
    fwd_rate = 5e8
)

subs = m.Subsystem()
subs.add_species(a)
subs.add_species(b)
subs.add_species(c)
subs.add_reaction_rule(react_a_and_b)


# ------- instantiation_data ---------
 
# ---- box ----
box_vertex_list = [
    [-0.05, -0.05, 0.05], 
    [-0.05, 0.05, -0.05], 
    [-0.05, -0.05, -0.05], 
    [-0.05, 0.05, 0.05], 
    [0.05, 0.05, -0.05], 
    [0.05, 0.05, 0.05], 
    [0.05, -0.05, -0.05], 
    [0.05, -0.05, 0.05]
] # box_vertex_list

box_element_connections = [
    [0, 1, 2], 
    [3, 4, 1], 
    [5, 6, 4], 
    [7, 2, 6], 
    [4, 2, 1], 
    [3, 7, 5], 
    [0, 3, 1], 
    [3, 5, 4], 
    [5, 7, 6], 
    [7, 0, 2], 
    [4, 6, 2], 
    [3, 0, 7]
] # box_element_connections

box = m.GeometryObject(
    name = 'box',
    vertex_list = box_vertex_list,
    element_connections = box_element_connections
)
# ^^^^ box ^^^^
 
 
rel_a = m.ReleaseSite(
    name = 'rel_a',
    species = a,
    shape = m.Shape.Spherical, # second option is shape which accepts geometry object or region?, or use names?
    location = m.Vec3(0, 0, 0),
    number_to_release = 100
)
 
rel_b = m.ReleaseSite(
    name = 'rel_b',
    shape = m.Shape.Spherical, # second option is shape which accepts geometry object or region?, or use names?
    location = m.Vec3(0.005, 0, 0),
    species = b,
    number_to_release = 100
)
 
inst = m.InstantiationData()

inst.add_geometry_object(box)
inst.add_release_site(rel_a)
inst.add_release_site(rel_b) # TODO: lists will be allowed as well

# ------- observables ---------

viz_output = m.VizOutput(
    mode = m.VizMode.Ascii,
    filename_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    species_list = [a, b, c]
)

observables = m.Observables()
observables.add_viz_output(viz_output)


model = m.Model()
model.add_subsystem(subs)
model.add_instantiation_data(inst)
model.add_observables(observables)

model.config.time_step = 1e-6 # default
model.config.seed = SEED
model.config.total_iterations_hint = ITERATIONS

model.config.partition_dimension = 20 + m.PARTITION_EDGE_EXTRA_MARGIN_UM * 2
model.config.subpartition_dimension = 2

model.initialize()

model.dump_internal_state()

model.run_iterations(ITERATIONS)
model.end_simulation()
