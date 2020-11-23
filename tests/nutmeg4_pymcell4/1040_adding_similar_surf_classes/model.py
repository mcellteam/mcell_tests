#!/usr/bin/env python3

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

# single property
sc1 = m.SurfaceClass(
    'sc', 
    type = m.SurfacePropertyType.REFLECTIVE,
    affected_complex_pattern = m.Complex('X(y!1).Y(x!1)')
)

sc2 = m.SurfaceClass(
    'sc', 
    type = m.SurfacePropertyType.TRANSPARENT,
    affected_complex_pattern = m.Complex('X(y!1).Y(x!1)')
)

sub1 = m.Subsystem()
sub1.add_surface_class(sc1)
# error
try:
    sub1.add_surface_class(sc2)
    assert False
except ValueError as err:
    print(err)



sc3 = m.SurfaceClass(
    'sc', 
    type = m.SurfacePropertyType.TRANSPARENT,
    affected_complex_pattern = m.Complex('Y(x!1).X(y!1)')
)

sub2 = m.Subsystem()
sub2.add_surface_class(sc2)
# warning
sub2.add_surface_class(sc3)



# multiple properties
p1_1 = m.SurfaceProperty(
    type = m.SurfacePropertyType.REFLECTIVE,
    affected_complex_pattern = m.Complex('X(y!1).Y(x!1)')
)

p1_2 = m.SurfaceProperty(
    type = m.SurfacePropertyType.REFLECTIVE,
    affected_complex_pattern = m.Complex('Y(x!1).X(y!1)')
)

p2 = m.SurfaceProperty(
    type = m.SurfacePropertyType.CONCENTRATION_CLAMP,
    affected_complex_pattern = m.Complex('Y(x!1).X(y!1)'),
    concentration = 1e5
)

sc4 = m.SurfaceClass('sc_props', properties = [p1_1, p2])
sc5 = m.SurfaceClass('sc_props', properties = [p2, p1_2])

sub3 = m.Subsystem()
sub3.add_surface_class(sc4)
# warning
sub3.add_surface_class(sc5)



p3 = m.SurfaceProperty(
    type = m.SurfacePropertyType.CONCENTRATION_CLAMP,
    affected_complex_pattern = m.Complex('Y(x!1).X(y!1)'),
    concentration = 1e6
)

sc6 = m.SurfaceClass('sc_props2', properties = [p2])
sc7 = m.SurfaceClass('sc_props2', properties = [p3])

sub4 = m.Subsystem()
sub4.add_surface_class(sc6)
# error
try:
    sub4.add_surface_class(sc7)
    assert False
except ValueError as err:
    print(err)

