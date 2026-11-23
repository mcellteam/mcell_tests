#!/usr/bin/env python3

# Every vertex or wall index that a Python API model passes to a getter, to
# set_wall_color or to add_vertex_move is checked: below 0 or not below the
# object's vertex or wall count gives a RuntimeError that names the list
# (mcell step 12b). add_vertex_move used to end Python at an assertion for -1
# on the model's first object and for an index past the model's last vertex,
# and the wall check's text named a vertex. Geometry only: no volume or surface
# molecules are involved.

import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m

# two 1 um cubes, 8 vertices and 12 walls each; box is the model's first object
box = m.geometry_utils.create_box('box', 1.0)
box2 = m.geometry_utils.create_box('box2', 1.0)
box2.translate([3, 0, 0])

model = m.Model()
model.add_geometry_object(box)
model.add_geometry_object(box2)
model.config.total_iterations = 2
model.initialize()


def assert_raises(error_type, text, function, *args):
    try:
        function(*args)
    except error_type as e:
        assert str(e) == text, 'unexpected text: ' + str(e)
        return
    assert False, 'expected ' + error_type.__name__ + ': ' + text


red = m.Color(red=1, green=0, blue=0, alpha=1)

for obj in [box, box2]:
    for i in [-1, 8, 99]:
        text = 'Vertex index ' + str(i) + ' is out of range for vertex_list of ' + obj.name + '.'
        assert_raises(RuntimeError, text, model.get_vertex, obj, i)
        assert_raises(RuntimeError, text, model.get_vertex_unit_normal, obj, i)
        assert_raises(RuntimeError, text, model.add_vertex_move, obj, i, [0, 0, 0.1])

    for i in [-1, 12, 99]:
        text = 'Wall index ' + str(i) + ' is out of range for wall_list of ' + obj.name + '.'
        assert_raises(RuntimeError, text, model.get_wall, obj, i)
        assert_raises(RuntimeError, text, model.get_wall_unit_normal, obj, i)
        assert_raises(RuntimeError, text, model.get_wall_color, obj, i)
        assert_raises(RuntimeError, text, model.set_wall_color, obj, i, red)

# the index is checked before the displacement
assert_raises(
    RuntimeError, 'Vertex index -1 is out of range for vertex_list of box.',
    model.add_vertex_move, box, -1, [0, 0])

# the last valid indices still work, and no vertex move was added above
assert len(model.get_vertex(box2, 7)) == 3
assert len(model.get_vertex_unit_normal(box2, 7)) == 3
assert model.get_wall(box2, 11).wall_index == 11
assert len(model.get_wall_unit_normal(box2, 11)) == 3
model.set_wall_color(box2, 11, red)
assert model.get_wall_color(box2, 11).red == 1

v = model.get_vertex(box, 0)
model.add_vertex_move(box, 0, [0, 0, -0.1])
model.apply_vertex_moves()
moved = model.get_vertex(box, 0)
assert abs(moved[0] - v[0]) < 1e-9 and abs(moved[1] - v[1]) < 1e-9
assert abs(moved[2] - (v[2] - 0.1)) < 1e-9

model.run_iterations(2)
model.end_simulation()
