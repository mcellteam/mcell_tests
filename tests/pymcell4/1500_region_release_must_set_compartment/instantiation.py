# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----


Release_of_Syk_ps_a_Y_l_Y_tSH2_pe_CP_at_CP = m.ReleaseSite(
    name = 'Release_of_Syk_ps_a_Y_l_Y_tSH2_pe_CP_at_CP',
    complex = m.Complex('Syk(a~Y,l~Y,tSH2)'),
    region = CP,
    number_to_release = 20
)



# ---- surface classes assignment ----

# ---- compartments assignment ----

default_compartment.is_bngl_compartment = True

EC.is_bngl_compartment = True

CP.is_bngl_compartment = True
CP.surface_compartment_name = 'PM'

# ---- create instantiation object and add components ----

instantiation = m.Instantiation()
instantiation.add_geometry_object(default_compartment)
#instantiation.add_geometry_object(EC)
instantiation.add_geometry_object(CP)
#instantiation.add_release_site(Release_of_Lig_ps_l_l_pe_EC_at_EC)
#instantiation.add_release_site(Release_of_Lyn_ps_SH2_U_pe_PM_at_PM)
instantiation.add_release_site(Release_of_Syk_ps_a_Y_l_Y_tSH2_pe_CP_at_CP)
#instantiation.add_release_site(Release_of_Rec_ps_a_b_Y_g_Y_pe_PM_at_PM)
