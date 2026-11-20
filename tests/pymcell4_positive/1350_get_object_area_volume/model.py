#!/usr/bin/env python3

# Model.get_object_area and Model.get_object_volume.
#
# Geometry only: there are no volume or surface molecules, since the two
# getters read only the objects' meshes.
#
# Five objects, made from the lists of geometry_utils.create_box, each placed
# apart from the others:
# - box: a 1 um cube; area 6 um^2, volume 1 um^3;
# - inside_out_box: the same cube with every wall reversed, so that it faces
#   inward; area 6 um^2, signed volume -1 um^3. No count, compartment or
#   release uses it, so it is listed only in the geometry report;
# - box_with_cavity: one object of two shells, a 2 um cube and, inside it, a
#   1 um cube that faces inward (a cavity); area 24 + 6 = 30 um^2, volume
#   8 - 1 = 7 um^3;
# - box_without_top: the 1 um cube without its top face, 10 walls and 4
#   boundary edges; area 5 um^2. It is non-watertight, so it has no volume and
#   get_object_volume raises a ValueError;
# - moved_box: a 1 um cube whose top face moves up 1 um after the first
#   iteration; area 6 um^2 and volume 1 um^3 before the move, area
#   4 * 2 + 2 * 1 = 10 um^2 and volume 2 um^3 after it.
#
# The expected values are worked out by hand. Each object's area is also
# compared with the sum of its walls' areas from Model.get_wall. Before
# initialization, and with None, both getters raise.

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m


def cube_lists(edge_length, shift, reverse_walls=False, remove_top=False):
    box = m.geometry_utils.create_box('tmp', edge_length)
    vertices = [[v[0] + shift[0], v[1] + shift[1], v[2] + shift[2]] for v in box.vertex_list]
    walls = [[w[0], w[1], w[2]] for w in box.wall_list]
    if remove_top:
        # the two walls of the top face, whose vertices all have the largest z
        top_z = shift[2] + edge_length / 2
        walls = [w for w in walls if not all(vertices[i][2] == top_z for i in w)]
    if reverse_walls:
        walls = [[w[0], w[2], w[1]] for w in walls]
    return vertices, walls


v, w = cube_lists(1, [0, 0, 0])
box = m.GeometryObject(name = 'box', vertex_list = v, wall_list = w)

v, w = cube_lists(1, [2.5, 0, 0], reverse_walls = True)
inside_out_box = m.GeometryObject(name = 'inside_out_box', vertex_list = v, wall_list = w)

v_outer, w_outer = cube_lists(2, [-3, 0, 0])
v_inner, w_inner = cube_lists(1, [-3, 0, 0], reverse_walls = True)
n = len(v_outer)
box_with_cavity = m.GeometryObject(
    name = 'box_with_cavity',
    vertex_list = v_outer + v_inner,
    wall_list = w_outer + [[i + n, j + n, k + n] for i, j, k in w_inner]
)

v, w = cube_lists(1, [0, 2.5, 0], remove_top = True)
box_without_top = m.GeometryObject(name = 'box_without_top', vertex_list = v, wall_list = w)
assert len(box_without_top.wall_list) == 10

v, w = cube_lists(1, [0, -2.5, 0])
moved_box = m.GeometryObject(name = 'moved_box', vertex_list = v, wall_list = w)

objects = [box, inside_out_box, box_with_cavity, box_without_top, moved_box]

model = m.Model()
for o in objects:
    model.add_geometry_object(o)


def assert_eq(a, b):
    assert abs(a - b) < 1e-8, str(a) + ' != ' + str(b)


def assert_raises(error_type, text, function, *args):
    try:
        function(*args)
    except error_type as e:
        assert str(e) == text, 'unexpected text: ' + str(e)
        return
    assert False, 'expected ' + error_type.__name__ + ': ' + text


# before initialization the objects aren't in the model yet
NOT_PRESENT = 'Geometry object box is not present in model (or model was not initialized).'
assert_raises(RuntimeError, NOT_PRESENT, model.get_object_area, box)
assert_raises(RuntimeError, NOT_PRESENT, model.get_object_volume, box)

# ---- initialization and execution ----

model.initialize()

NONE_ARGUMENT = 'Argument passed as GeometryObject must not be None.'
assert_raises(ValueError, NONE_ARGUMENT, model.get_object_area, None)
assert_raises(ValueError, NONE_ARGUMENT, model.get_object_volume, None)

NON_WATERTIGHT = \
    'Geometry object box_without_top is non-watertight (4 boundary edges), so it has no volume; ' \
    'see reports/geometry_report_00001.txt'


# expected: (object, area in um^2, volume in um^3 or None when non-watertight)
def check(expected):
    for o, area, volume in expected:
        assert_eq(model.get_object_area(o), area)
        assert_eq(sum(model.get_wall(o, i).area for i in range(len(o.wall_list))), area)
        if volume is None:
            assert_raises(ValueError, NON_WATERTIGHT, model.get_object_volume, o)
        else:
            assert_eq(model.get_object_volume(o), volume)


before_move = [
    (box, 6, 1),
    (inside_out_box, 6, -1),
    (box_with_cavity, 30, 7),
    (box_without_top, 5, None),
    (moved_box, 6, 1)
]

check(before_move)
model.run_iterations(1)
check(before_move)

# the top face of moved_box goes up by 1 um
for i, v in enumerate(moved_box.vertex_list):
    if v[2] == 0.5:
        model.add_vertex_move(moved_box, i, [0, 0, 1])
hits = model.apply_vertex_moves()
assert len(hits) == 0

after_move = before_move[:4] + [(moved_box, 10, 2)]

check(after_move)
model.run_iterations(1)
check(after_move)

model.end_simulation()
