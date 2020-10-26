import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----

Release_Site_1 = m.ReleaseSite(
    name = 'Release_Site_1',
    complex = m.Complex('A', compartment_name = 'EC'),
    region = EC,
    number_to_release = 1000
)

Release_Site_2 = m.ReleaseSite(
    name = 'Release_Site_2',
    complex = m.Complex('Mem', compartment_name = 'PM'),
    orientation = m.Orientation.UP,
    region = CP,
    number_to_release = 1000
)

# ---- surface classes assignment ----

EC.surface_class = reflect
CP.surface_class = reflect

# ---- compartments assignment ----

CP.is_bngl_compartment = True
CP.surface_compartment_name = 'PM'

EC.is_bngl_compartment = True

# ---- instantiation data ----

instantiation = m.InstantiationData()
instantiation.add_geometry_object(CP)
instantiation.add_geometry_object(EC)
instantiation.add_release_site(Release_Site_1)
instantiation.add_release_site(Release_Site_2)
