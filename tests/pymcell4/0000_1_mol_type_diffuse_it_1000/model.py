#!/usr/bin/env python3

# based on mcell_tests/tests/mdl/0000_1_mol_type_diffuse_it_1000

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

# only temporary check
libpath = os.path.join(MCELL_DIR, 'lib', 'mcell.so')
if not os.path.exists(libpath):
    print("Error: library " + libpath + " was not found.")
    sys.exit(1)

import mcell as m

SEED = 1
ITERATIONS = 1000

# ------- subsystem ---------

a = m.Species('a', diffusion_constant_3d = 1e-6)

subs = m.Subsystem()
subs.add_species(a)

#print(subs)


# ------- instantiation_data ---------

rel_a = m.ReleaseSite(
    name = 'rel_a',
    species = a,
    shape = m.Shape.Spherical,
    location = m.Vec3(0, 0, 0),
    site_diameter = 0, # default
    number_to_release = 2
)

instantiation_data = m.InstantiationData()
instantiation_data.add_release_site(rel_a)


# ------- observables ---------

viz_output = m.VizOutput(
    filename_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    species_list = [a] 
)

observables = m.Observables()
# TODO: there must not be viz outputs with the same filename
observables.add_viz_output(viz_output)


model = m.Model()
model.add_subsystem(subs)
model.add_instantiation_data(instantiation_data)
model.add_observables(observables)

model.config.time_step = 1e-6 # default
model.config.seed = SEED
model.config.total_iterations_hint = ITERATIONS

#model.dump()

# initialization 'locks' parameters of the model that cannot be changed
# during simulation
# also does final semantic check
  
model.initialize()

#model.dump_internal_state()

model.run_iterations(ITERATIONS)

model.end_simulation()


