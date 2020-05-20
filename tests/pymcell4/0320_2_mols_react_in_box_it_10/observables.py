import mcell as m

from parameters import *
from subsystem import *
from instantiation import *

# This generated file defines the following objects:
# viz_output: m.VizOutput
# observables: m.Observables

# ------- observables ---------

viz_output = m.VizOutput(
    mode = m.VizMode.Ascii,
    filename_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    species_list = [a, b, c]
)

observables = m.Observables()
observables.add_viz_output(viz_output)