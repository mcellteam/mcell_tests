import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- observables ----

viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(get_seed()).zfill(5) + '/Scene',
    all_species = True,
    every_n_timesteps = 1
)

count_A_at_EC = m.Count(
    molecules_pattern = A.inst(compartment_name = 'EC'),
    file_name = './react_data/seed_' + str(get_seed()).zfill(5) + '/aec.dat'
)

count_A_at_CP = m.Count(
    molecules_pattern = A.inst(compartment_name = 'CP'),
    file_name = './react_data/seed_' + str(get_seed()).zfill(5) + '/acp.dat'
)

count_B_at_CP = m.Count(
    molecules_pattern = B.inst(compartment_name = 'CP'),
    file_name = './react_data/seed_' + str(get_seed()).zfill(5) + '/bcp.dat'
)

count_Mem = m.Count(
    molecules_pattern = Mem.inst(),
    file_name = './react_data/seed_' + str(get_seed()).zfill(5) + '/mem.dat'
)

count_B_at_EC = m.Count(
    molecules_pattern = B.inst(compartment_name = 'EC'),
    file_name = './react_data/seed_' + str(get_seed()).zfill(5) + '/bec.dat'
)

observables = m.Observables()
observables.add_viz_output(viz_output)
observables.add_count(count_A_at_EC)
observables.add_count(count_A_at_CP)
observables.add_count(count_B_at_CP)
observables.add_count(count_Mem)
observables.add_count(count_B_at_EC)
