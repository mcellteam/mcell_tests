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
    every_n_timesteps = SAMPLING_PERIODICITY
)


# ---- create observables object and add components ----

observables = m.Observables()

observables.load_bngl_observables('model.bngl', './react_data/seed_' + str(SEED).zfill(5) + '/')

for count in observables.counts:
    count.every_n_timesteps = SAMPLING_PERIODICITY

observables.add_viz_output(viz_output)
