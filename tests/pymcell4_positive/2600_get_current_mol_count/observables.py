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
react_a_plus_b = subsystem.find_reaction_rule('react_a_plus_b')
assert react_a_plus_b, "Reaction rule 'react_a_plus_b' was not found"

react_b_plus_c = subsystem.find_reaction_rule('react_b_plus_c')
assert react_b_plus_c, "Reaction rule 'react_b_plus_c' was not found"


count_a_Cube1 = m.Count(
    molecules_pattern = m.Complex('a'),
    region = Cube1,
    file_name = './react_data/seed_' + str(get_seed()).zfill(5) + '/a.Cube1.dat',
    every_n_timesteps = 0 # used only manually
)

count_a_Cube2 = m.Count(
    molecules_pattern = m.Complex('a'),
    region = Cube2,
    file_name = './react_data/seed_' + str(get_seed()).zfill(5) + '/a.Cube2.dat',
    every_n_timesteps = 0 # used only manually
)

count_a_Cube3 = m.Count(
    molecules_pattern = m.Complex('a'),
    region = Cube3,
    file_name = './react_data/seed_' + str(get_seed()).zfill(5) + '/a.Cube3.dat',
    every_n_timesteps = 0 # used only manually
)


observables = m.Observables()
observables.add_viz_output(viz_output)
observables.add_count(count_a_Cube1)
observables.add_count(count_a_Cube2)
observables.add_count(count_a_Cube3)

# load observables information from bngl file
observables.load_bngl_observables('model.bngl', subsystem, './react_data/seed_' + str(get_seed()).zfill(5) + '/')
