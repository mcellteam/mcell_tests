# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *
from subsystem import *
from geometry import *
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))


# ---- observables ----

viz_output = m.VizOutput(
    mode = m.VizMode.CELLBLENDER,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 100
)

# ---- declaration of rxn rules defined in BNGL and used in counts ----

cterm_count_a_species = m.CountTerm(
    species_pattern = m.Complex('a')
)

count_a_World = m.Count(
    name = 'a_World',
    expression = cterm_count_a_species,
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/a_World.dat',
    every_n_timesteps = 1e3/1e-6
)
"""
cterm_count_b_species = m.CountTerm(
    species_pattern = m.Complex('b')
)

count_b_World = m.Count(
    name = 'b_World',
    expression = cterm_count_b_species,
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/b_World.dat',
    every_n_timesteps = 1e4/1e-6
)

cterm_count_c_species = m.CountTerm(
    species_pattern = m.Complex('c')
)

count_c_World = m.Count(
    name = 'c_World',
    expression = cterm_count_c_species,
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/c_World.dat',
    every_n_timesteps = 1e4/1e-6
)
"""

# ---- create observables object and add components ----

observables = m.Observables()
observables.add_viz_output(viz_output)
observables.add_count(count_a_World)
#observables.add_count(count_b_World)
#observables.add_count(count_c_World)
