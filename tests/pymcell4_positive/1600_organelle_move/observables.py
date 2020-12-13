import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- observables ----

viz_output = m.VizOutput(
    mode = m.VizMode.CELLBLENDER,
    output_files_prefix = './viz_data/seed_' + str(get_seed()).zfill(5) + '/Scene',
    every_n_timesteps = 1
)

# declaration of rxn rules defined in BNGL and used in counts

observables = m.Observables()
observables.add_viz_output(viz_output)

# load observables information from bngl file
observables.load_bngl_observables('model.bngl', subsystem, './react_data/seed_' + str(get_seed()).zfill(5) + '/')
