# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *
from subsystem import *
from geometry import *
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))


observables = m.Observables()


# ---- observables ----

viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)


variants = [
    ('World', None), ('Outer', Outer), 
    ('OuterTransp', OuterTransp), ('InnerTransp', InnerTransp), ('InnerTransp2', InnerTransp2)]

for mol in ['a', 'b']:
    for v in variants:
        cnt = m.Count(
            name = mol + '_' + v[0],
            expression = m.CountTerm(
                species_pattern = m.Complex(mol),
                region = v[1]
            )
        )
        observables.add_count(cnt)


# ---- declaration of rxn rules defined in BNGL and used in counts ----

# ---- create observables object and add components ----

observables.add_viz_output(viz_output)
