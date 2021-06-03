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


rxn = subsystem.find_reaction_rule('a_plus_b')
assert rxn

count_all = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.all.dat',
    every_n_timesteps = 1
)

count_box1 = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn,
        region = box1
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.box1.dat',
    every_n_timesteps = 1
)

count_box1_sr1 = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn,
        region = box1_sr1
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.box1_sr1.dat',
    every_n_timesteps = 1
)

count_box1_sr2 = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn,
        region = box1_sr2
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.box1_sr2.dat',
    every_n_timesteps = 1
)

count_box1_sr1_only = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn,
        region = box1_sr1 - box1_sr2
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.box1_sr1_only.dat',
    every_n_timesteps = 1
)

count_box1_sr2_only = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn,
        region = box1_sr2 - box1_sr1
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.box1_sr2_only.dat',
    every_n_timesteps = 1
)

count_box1_sr1_and_sr2 = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn,
        region = box1_sr1 * box1_sr2
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.box1_sr1_and_sr2.dat',
    every_n_timesteps = 1
)


count_box2 = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn,
        region = box2
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.box2.dat',
    every_n_timesteps = 1
)

count_box1_or_box2 = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn,
        region = box1 + box2
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.box1_or_box2.dat',
    every_n_timesteps = 1
)


count_box1_minus_box2 = m.Count(
    expression = m.CountTerm(
        reaction_rule = rxn,
        region = box1 - box2
    ),
    file_name = './react_data/seed_' + str(SEED).zfill(5) + '/rxn.box1_or_box2.dat',
    every_n_timesteps = 1
)


# ---- create observables object and add components ----

observables = m.Observables()
observables.add_viz_output(viz_output)
observables.add_count(count_all)

observables.add_count(count_box1)
observables.add_count(count_box1_sr1)
observables.add_count(count_box1_sr2)
observables.add_count(count_box2)
observables.add_count(count_box1_or_box2)

observables.add_count(count_box1_sr1_only)
observables.add_count(count_box1_sr2_only)
observables.add_count(count_box1_sr1_and_sr2)

