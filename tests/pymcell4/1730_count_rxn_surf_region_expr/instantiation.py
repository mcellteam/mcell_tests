# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *
from subsystem import *
from geometry import *
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

instantiation = m.Instantiation()
for mol in ['A', 'B']:
    cplx = m.Complex(mol)
    
    box1_sr1_rel = m.ReleaseSite(
        name = 'box1_sr1_rel_' + mol,
        complex = cplx,
        region = box1_sr1,
        number_to_release = 40
    )
    
    box1_sr2_rel = m.ReleaseSite(
        name = 'box1_sr2_rel' + mol,
        complex = cplx,
        region = box1_sr2,
        number_to_release = 60
    )
    
    box2_rel = m.ReleaseSite(
        name = 'box2_rel' + mol,
        complex = cplx,
        region = box2,
        number_to_release = 30
    )

    instantiation.add_release_site(box1_sr1_rel)
    instantiation.add_release_site(box1_sr2_rel)
    instantiation.add_release_site(box2_rel)


instantiation.add_geometry_object(box1)
instantiation.add_geometry_object(box2)
