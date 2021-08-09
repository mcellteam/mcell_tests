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
    every_n_timesteps = 1
)

# ---- declaration of rxn rules defined in BNGL and used in counts ----

cterm_count_a_species_Cube1 = m.CountTerm(
    species_pattern = m.Complex('a'),
    region = Cube1
)

count_a_Cube1 = m.Count(
    name = 'a_Cube1',
    expression = cterm_count_a_species_Cube1,
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/a_Cube1.dat'
)

cterm_count_b_species_Cube2 = m.CountTerm(
    species_pattern = m.Complex('b'),
    region = Cube2
)

count_b_Cube2 = m.Count(
    name = 'b_Cube2',
    expression = cterm_count_b_species_Cube2,
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/b_Cube2.dat'
)

# ---- create observables object and add components ----

observables = m.Observables()
observables.add_viz_output(viz_output)
observables.add_count(count_a_Cube1)
observables.add_count(count_b_Cube2)
