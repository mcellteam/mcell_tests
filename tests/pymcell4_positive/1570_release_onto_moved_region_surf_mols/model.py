#!/usr/bin/env python3
"""
Surface molecules released onto a surface region after its walls have moved
(mcell step 7a): the number released by density comes from the region's area
after the move, the molecules are spread over the walls by their areas after the
move, and the removal of molecules (a negative number) takes them from the whole
region.

A 1 um cube with the surface region 'sides', its four side faces. After
iteration 1 its top face moves up by 1 um, so that the sides go from 4 to 8 um^2
and reach up to z = 1.5 um. Surface molecules that don't diffuse, one species
per release:
- s0: 100/um^2 by density at time 0, before the move: 400 molecules;
- s1: 100/um^2 by density at iteration 2: 800 molecules, from the area after the
  move;
- s2: 1000 by number at iteration 2;
- 500 molecules s2 removed at iteration 3.

After each run the model writes, for each species, the number of molecules and
how many lie above z = 0.5 um (the part that the move added) to
react_data/seed_<seed>/release_summary.txt, which the test compares with its
reference.

Before step 7a, s1 got 400 molecules (the area before the move), most of them
below z = 0.5 um.
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

box = m.geometry_utils.create_box('box', 1.0)  # from -0.5 to 0.5 um

# the walls with vertices below and above z = 0
side_walls = [
    wi for wi, w in enumerate(box.wall_list)
    if min(box.vertex_list[v][2] for v in w) < 0 < max(box.vertex_list[v][2] for v in w)]
assert len(side_walls) == 8
sides = m.SurfaceRegion('sides', wall_indices=side_walls)
box.surface_regions = [sides]

species = [m.Species('s' + str(i), diffusion_constant_2d=0) for i in range(3)]
s0, s1, s2 = species

model = m.Model()
model.add_geometry_object(box)
for s in species:
    model.add_species(s)


def up(s):
    return m.Complex(s.name, orientation=m.Orientation.UP)


model.add_release_site(m.ReleaseSite(
    name='rel_s0', complex=up(s0), region=sides, density=100, release_time=0))
model.add_release_site(m.ReleaseSite(
    name='rel_s1', complex=up(s1), region=sides, density=100, release_time=2e-6))
model.add_release_site(m.ReleaseSite(
    name='rel_s2', complex=up(s2), region=sides, number_to_release=1000, release_time=2e-6))
model.add_release_site(m.ReleaseSite(
    name='remove_s2', complex=up(s2), region=sides, number_to_release=-500, release_time=3e-6))

model.config.total_iterations = 4
model.config.seed = SEED
model.initialize()

out_dir = os.path.join('react_data', 'seed_' + str(SEED).zfill(5))
os.makedirs(out_dir, exist_ok=True)
summary = open(os.path.join(out_dir, 'release_summary.txt'), 'w')
summary.write('# iteration species molecules above_z_0.5_um\n')


def on_moved_sides(p):
    on_x_face = abs(abs(p[0]) - 0.5) < 1e-6 and abs(p[1]) <= 0.5
    on_y_face = abs(abs(p[1]) - 0.5) < 1e-6 and abs(p[0]) <= 0.5
    return (on_x_face or on_y_face) and -0.5 <= p[2] <= 1.5


# number of molecules and number above z = 0.5 um, per species
def summarize(iteration):
    res = {}
    for s in species:
        positions = [model.get_molecule(i).pos3d for i in model.get_molecule_ids(pattern=m.Complex(s.name))]
        assert all(on_moved_sides(p) for p in positions)
        res[s.name] = (len(positions), sum(1 for p in positions if p[2] > 0.5))
        summary.write('%d %s %d %d\n' % ((iteration, s.name) + res[s.name]))
    return res


model.run_iterations(1)
r = summarize(1)
assert r['s0'] == (400, 0)
assert r['s1'][0] == 0 and r['s2'][0] == 0

# the top face moves up by 1 um
for i, v in enumerate(box.vertex_list):
    if v[2] > 0:
        model.add_vertex_move(box, i, [0, 0, 1.0])
model.apply_vertex_moves(randomize_order=False)

model.run_iterations(2)
r = summarize(3)
assert r['s0'][0] == 400
assert r['s1'][0] == 800
assert r['s2'][0] == 1000
for name in ['s1', 's2']:
    assert r[name][1] > 0, name + ' has no molecule in the part that the move added'
s2_above_before_removal = r['s2'][1]

model.run_iterations(1)
r = summarize(4)
assert r['s2'][0] == 500
assert 0 < r['s2'][1] < s2_above_before_removal, 'the removal took no molecule s2 from the part that the move added'

summary.close()
model.end_simulation()
