#!/usr/bin/env python3
"""
Counting inside counted objects that intersect each other, after a vertex move
(mcell step 7a, 3B): once vertices have moved, a volume molecule's counted
volume comes from the walls' current positions.

Only volume molecules: a, which diffuses, and b, which doesn't; there are no
surface molecules. Boxes X (1 um, centered at the origin) and Y (1 um, centered
at (-0.2, 0.5, 0.3)) intersect, both are counted, and both are transparent for
a. 1000 molecules a are released at time 0 next to X's +x face, outside X and
Y. After iteration 50, X's +x face moves from x = 0.5 to x = 1 um: the moving
face pushes the molecules a in its way along, and X now holds part of the space
around them. At iteration 51, 100 molecules b are released at one point inside
that added part of X, outside Y. After every iteration, each count must equal
the number of molecules inside each box by position (as in test 2610), and b
must be counted 100 times in X and never in Y.

In a model with intersecting counted objects, the counted volume of a new
molecule, or of one that crosses a wall of such an object, used to be copied
from the nearest waypoint (the center of its subpartition) when no counted wall
lies between them. Waypoints are set at initialization and not after vertex
moves, so after the move the molecules b, and the molecules a that came back
into the added part, were counted outside X (b: 0 instead of 100).
"""

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

SEED = 1
if len(sys.argv) == 3 and sys.argv[1] == '-seed':
    SEED = int(sys.argv[2])

ITERATIONS = 200
MOVE_AFTER = 50
SHIFT = 0.5  # um, X's +x face moves from x = 0.5 to 1

# name: (edge length, center), in um
BOXES = {
    'X': (1.0, (0, 0, 0)),
    'Y': (1.0, (-0.2, 0.5, 0.3))
}

model = m.Model()

a = m.Species(name='a', diffusion_constant_3d=1e-5)
b = m.Species(name='b', diffusion_constant_3d=0)
model.add_species(a)
model.add_species(b)

transparent = m.SurfaceClass(
    name='transparent', type=m.SurfacePropertyType.TRANSPARENT, affected_complex_pattern=m.Complex('a'))
model.add_surface_class(transparent)

boxes = {}
for name, (size, center) in BOXES.items():
    box = m.geometry_utils.create_box(name, size)
    box.vertex_list = [[v[i] + center[i] for i in range(3)] for v in box.vertex_list]
    box.surface_class = transparent
    model.add_geometry_object(box)
    boxes[name] = box
    for s in ['a', 'b']:
        model.add_count(m.Count(
            name=s + '_in_' + name,
            expression=m.CountTerm(species_pattern=m.Complex(s), region=box),
            file_name='./react_data/seed_' + str(SEED).zfill(5) + '/' + s + '_in_' + name + '.dat',
            every_n_timesteps=1
        ))

# next to X's +x face, outside X and Y
model.add_release_site(m.ReleaseSite(
    name='rel_a', complex=m.Complex('a'), shape=m.Shape.SPHERICAL,
    location=[0.75, 0, 0], site_diameter=0.2, number_to_release=1000
))
# at one point of the part that the move adds to X, outside Y; a release at the
# time of iteration 50 runs in iteration 51, after the move
model.add_release_site(m.ReleaseSite(
    name='rel_b', complex=m.Complex('b'), shape=m.Shape.SPHERICAL,
    location=[0.7, 0.2, 0.2], site_diameter=0, number_to_release=100,
    release_time=MOVE_AFTER * 1e-6
))

model.config.total_iterations = ITERATIONS
model.config.seed = SEED
model.initialize()

x_face = 0.5  # X's +x face


def is_inside(pos, name):
    size, center = BOXES[name]
    lo = [center[i] - size / 2 for i in range(3)]
    hi = [center[i] + size / 2 for i in range(3)]
    if name == 'X':
        hi[0] = x_face
    return all(lo[i] < pos[i] < hi[i] for i in range(3))


a_in_x_before_move = None
a_in_added_part = 0
for it in range(1, ITERATIONS + 1):
    model.run_iterations(1)

    if it == MOVE_AFTER:
        a_in_x_before_move = model.find_count('a_in_X').get_current_value()
        for i, v in enumerate(boxes['X'].vertex_list):
            if v[0] > 0:
                model.add_vertex_move(boxes['X'], i, [SHIFT, 0, 0])
        model.apply_vertex_moves(randomize_order=False)
        x_face = 0.5 + SHIFT

    for s in ['a', 'b']:
        positions = [model.get_molecule(id).pos3d for id in model.get_molecule_ids(pattern=m.Complex(s))]
        for name in BOXES:
            counted = model.find_count(s + '_in_' + name).get_current_value()
            expected = sum(is_inside(pos, name) for pos in positions)
            assert counted == expected, \
                'iteration %d, %s in box %s: counted %g, from positions %d' % (it, s, name, counted, expected)
        if s == 'a' and it > MOVE_AFTER:
            a_in_added_part = max(a_in_added_part, sum(1 for p in positions if is_inside(p, 'X') and p[0] > 0.5))

    if it > MOVE_AFTER:
        assert model.find_count('b_in_X').get_current_value() == 100, 'iteration %d' % it
        assert model.find_count('b_in_Y').get_current_value() == 0, 'iteration %d' % it

# the molecules a must have reached X and Y, and the part that the move added to
# X, for the test to mean anything
assert a_in_x_before_move > 0, 'no molecule a in X before the move'
assert model.find_count('a_in_Y').get_current_value() > 0, 'no molecule a in Y'
assert a_in_added_part > 0, 'no molecule a in the part that the move added to X'

model.end_simulation()
