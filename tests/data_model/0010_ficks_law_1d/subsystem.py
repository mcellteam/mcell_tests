import mcell as m

from parameters import *

# ---- subsystem ----

vm = m.Species(
    name = 'vm',
    diffusion_constant_3d = dc
)

transp = m.SurfaceClass(
    name = 'transp',
    type = m.SurfacePropertyType.TRANSPARENT,
    affected_species = vm
)

absorb = m.SurfaceClass(
    name = 'absorb',
    type = m.SurfacePropertyType.ABSORPTIVE,
    affected_species = vm
)

subsystem = m.Subsystem()
subsystem.add_species(vm)
subsystem.add_surface_class(transp)
subsystem.add_surface_class(absorb)
