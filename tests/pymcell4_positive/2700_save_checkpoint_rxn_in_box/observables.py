# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import mcell as m

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

from parameters import *
from subsystem import *
from geometry import *

# ---- observables ----

viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)


count_a = m.Count(
    file_name = 'a.dat',
    species_pattern = m.Complex('a')
)

# ---- create observables object and add components ----

observables = m.Observables()
observables.add_count(count_a)
observables.add_viz_output(viz_output)
