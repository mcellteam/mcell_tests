#!/usr/bin/env python3

# Counting inside counted objects that intersect each other and lie inside a
# third counted object. Boxes X and Y intersect, both lie inside box Z, and X
# and Y are transparent, so molecules cross their walls. After every iteration
# the counts must equal the numbers of molecules whose positions lie inside
# each box.
#
# MCell used to give a molecule that entered X an invalid counted volume
# (INTERSECTS), and counting then crashed: the outside of an intersecting
# object with a parent was the parent's volume, and the crossing code tested
# the outside index before assigning the inside index.

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

ITERATIONS = 200

# name: (edge length, center), in um
BOXES = {
    'Z': (4.0, (0, 0, 0)),
    'X': (1.0, (0, 0, 0)),
    'Y': (1.0, (0.5, 0.25, 0.25))
}

model = m.Model()

a = m.Species(name='a', diffusion_constant_3d=1e-5)
model.add_species(a)

transparent = m.SurfaceClass(
    name='transparent', type=m.SurfacePropertyType.TRANSPARENT, affected_complex_pattern=m.Complex('a'))
model.add_surface_class(transparent)

for name, (size, center) in BOXES.items():
    box = m.geometry_utils.create_box(name, size)
    box.vertex_list = [[v[i] + center[i] for i in range(3)] for v in box.vertex_list]
    if name != 'Z':
        box.surface_class = transparent
    model.add_geometry_object(box)
    model.add_count(m.Count(
        name='in_' + name,
        expression=m.CountTerm(species_pattern=m.Complex('a'), region=box),
        file_name='./react_data/seed_00001/in_' + name + '.dat',
        every_n_timesteps=1
    ))

# inside Z, next to the -x face of X, outside X and Y
model.add_release_site(m.ReleaseSite(
    name='rel', complex=m.Complex('a'), shape=m.Shape.SPHERICAL,
    location=[-0.8, 0, 0], site_diameter=0.4, number_to_release=1000
))

model.config.total_iterations = ITERATIONS
model.initialize()


def is_inside(pos, name):
    size, center = BOXES[name]
    return all(abs(pos[i] - center[i]) < size / 2 for i in range(3))


for it in range(1, ITERATIONS + 1):
    model.run_iterations(1)
    positions = [model.get_molecule(id).pos3d for id in model.get_molecule_ids()]
    for name in BOXES:
        counted = model.find_count('in_' + name).get_current_value()
        expected = sum(is_inside(pos, name) for pos in positions)
        assert counted == expected, \
            'iteration %d, box %s: counted %g, from positions %d' % (it, name, counted, expected)

# the molecules must have reached X and Y for the test to mean anything
for name in ('X', 'Y'):
    assert model.find_count('in_' + name).get_current_value() > 0, 'no molecule in ' + name

model.end_simulation()
