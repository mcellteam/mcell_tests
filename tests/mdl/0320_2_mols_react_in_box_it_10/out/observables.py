import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- observables ----

viz_output = m.VizOutput(
    mode = m.VizMode.Ascii,
    filename_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    species_list = [b, a, c],
    every_n_timesteps = 1
)

observables = m.Observables()
observables.add_viz_output(viz_output)
