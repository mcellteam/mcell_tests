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

count_a_Cube1 = m.Count(
    name = 'a_Cube1',
    expression = m.CountTerm(
        molecules_pattern = m.Complex('a'),
        region = Cube1
    )
)

count_a_Cube2 = m.Count(
    name = 'a_Cube2',
    expression = m.CountTerm(
        molecules_pattern = m.Complex('a'),
        region = Cube2 - Cube1 
    )
)

count_a_Cube3 = m.Count(
    name = 'a_Cube3',
    expression = m.CountTerm(
        molecules_pattern = m.Complex('a'),
        region = Cube3 - Cube2
    )
)

count_a_World = m.Count(
    name = 'a_World',
    expression = m.CountTerm(
        molecules_pattern = m.Complex('a')
    )
)



rxn_a_plus_b = subsystem.find_reaction_rule('rxn_a_plus_b')
assert rxn_a_plus_b

count_rxn_a_plus_b_World = m.Count(
    name = 'rxn_a_plus_b_World',
    expression = m.CountTerm(reaction_rule = rxn_a_plus_b)
) 

count_rxn_a_plus_b_Cube1 = m.Count(
    name = 'rxn_a_plus_b_Cube1',
    expression = m.CountTerm(
        reaction_rule = rxn_a_plus_b,
        region = Cube1 
    )
) 

count_rxn_a_plus_b_Cube2 = m.Count(
    name = 'rxn_a_plus_b_Cube2',
    expression = m.CountTerm(
        reaction_rule = rxn_a_plus_b,
        region = Cube2 - Cube1 
    )
) 

count_rxn_a_plus_b_Cube3 = m.Count(
    name = 'rxn_a_plus_b_Cube3',
    expression = m.CountTerm(
        reaction_rule = rxn_a_plus_b,
        region = Cube3 - Cube2 
    )
) 


observables = m.Observables()
observables.add_viz_output(viz_output)

observables.add_count(count_a_Cube1)
observables.add_count(count_a_Cube2)
observables.add_count(count_a_Cube3)
observables.add_count(count_a_World)


observables.add_count(count_rxn_a_plus_b_World)
observables.add_count(count_rxn_a_plus_b_Cube1)
observables.add_count(count_rxn_a_plus_b_Cube2)
observables.add_count(count_rxn_a_plus_b_Cube3)


# load observables information from bngl file
observables.load_bngl_observables('model.bngl', './react_data/seed_' + str(get_seed()).zfill(5) + '/')
