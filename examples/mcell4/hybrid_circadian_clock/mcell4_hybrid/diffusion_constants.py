
import mcell as m
import sys

UM2S_TO_CM2S = 1e-8
D1000 = 1000
D10 = 10
D0 = 0

MOLS_MRNA = ['A', 'AR', 'mRNA_A', 'mRNA_R']
PRMS = ['PrmA', 'PrmA_bound', 'PrmR', 'PrmR_bound']


def set_D(model, species_list, D):
    for s in species_list:
        emt = model.find_elementary_molecule_type(s)
        assert emt
        emt.diffusion_constant_3d = D * UM2S_TO_CM2S

def set_diffusion_constants(model, variant):
    if variant == 'D10_all':
        set_D(model, MOLS_MRNA, D10)
        set_D(model, PRMS, D10)
    elif variant == 'D1000_all':
        set_D(model, MOLS_MRNA, D1000)
        set_D(model, PRMS, D1000)
    elif variant == 'D10_prm_loc':
        set_D(model, MOLS_MRNA, D10)
        set_D(model, PRMS, D0)
    elif variant == 'D1000_prm_loc':
        set_D(model, MOLS_MRNA, D1000)
        set_D(model, PRMS, D0)
    else:
        exit("Invalid variant " + variant)
    