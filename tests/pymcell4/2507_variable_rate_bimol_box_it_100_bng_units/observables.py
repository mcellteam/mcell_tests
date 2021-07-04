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
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)

# ---- declaration of rxn rules defined in BNGL and used in counts ----

cterm_count_react_a_plus_b = m.CountTerm(
    reaction_rule = react_a_plus_b
)

count_react_a_plus_b_World = m.Count(
    name = 'react_a_plus_b.World',
    expression = cterm_count_react_a_plus_b,
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/react_a_plus_b.World.dat',
    every_n_timesteps = 9.99999999999999955e-07/1e-06
)

# ---- create observables object and add components ----

observables = m.Observables()
observables.add_viz_output(viz_output)
observables.add_count(count_react_a_plus_b_World)
