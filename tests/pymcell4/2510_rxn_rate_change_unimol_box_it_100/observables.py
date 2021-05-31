import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- observables ----

viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(get_seed()).zfill(5) + '/Scene',
    every_n_timesteps = 1
)

# declaration of rxn rules defined in BNGL and used in counts

count_react_a_plus_b = m.Count(
    expression = m.CountTerm(
        reaction_rule = subsystem.find_reaction_rule('a_to_b')
    ),
    file_name = './react_data/seed_' + str(get_seed()).zfill(5) + '/react_a_to_b.World.dat',
    every_n_timesteps = 9.99999999999999955e-07/1e-06
)

observables = m.Observables()
observables.add_viz_output(viz_output)
observables.add_count(count_react_a_plus_b)
