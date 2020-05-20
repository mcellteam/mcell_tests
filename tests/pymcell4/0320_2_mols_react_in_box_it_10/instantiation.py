import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# This generated file defines the following objects:
# rel_a: m.ReleaseSite
# rel_b: m.ReleaseSite
# instantiation: m.InstantiationData

# ------- instantiation_data ---------
 
rel_a = m.ReleaseSite(
    name = 'rel_a',
    species = a,
    shape = m.Shape.Spherical, # second option is shape which accepts geometry object or region?, or use names?
    location = m.Vec3(0, 0, 0),
    number_to_release = 100
)
 
rel_b = m.ReleaseSite(
    name = 'rel_b',
    shape = m.Shape.Spherical, # second option is shape which accepts geometry object or region?, or use names?
    location = m.Vec3(0.005, 0, 0),
    species = b,
    number_to_release = 100
)
 
instantiation = m.InstantiationData()

instantiation.add_geometry_object(box)
instantiation.add_release_site(rel_a)
instantiation.add_release_site(rel_b) # TODO: lists will be allowed as well