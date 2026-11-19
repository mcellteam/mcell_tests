#!/usr/bin/env python3
"""
Volume molecules released into a geometry object after its vertices have moved
(mcell step 7a): the number released by concentration comes from the object's
volume after the move, the positions come from the moved object, also for a
region expression, and the removal of molecules (a negative number) takes them
from the whole moved object.

A 1 um cube; after iteration 1 its top face moves up by 1 um, so that its volume
goes from 1 to 2 um^3 and its top from z = 0.5 to z = 1.5 um. A box of 0.4 um,
the hole, sits in the middle of the cube. Volume molecules that don't diffuse,
one species per release:
- a0: 1 uM by concentration at time 0, before the move: 602 molecules;
- a1: 1 uM by concentration at iteration 2: 1204 molecules, from the volume after
  the move;
- a2: 1000 by number at iteration 2;
- a3: 1000 by number into the cube minus the hole at iteration 2;
- 500 molecules a2 removed at iteration 3.

After each run the model writes, for each species, the number of molecules, how
many lie above z = 0.5 um (the part that the move added) and how many lie in the
hole to react_data/seed_<seed>/release_summary.txt, which the test compares with
its reference.

Before step 7a, a1 got 602 molecules (the volume before the move, computed for
a0's release), and every molecule released after the move lay below z = 0.5 um.
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

box = m.geometry_utils.create_box('box', 1.0)    # from -0.5 to 0.5 um
hole = m.geometry_utils.create_box('hole', 0.4)  # from -0.2 to 0.2 um

species = [m.Species('a' + str(i), diffusion_constant_3d=0) for i in range(4)]
a0, a1, a2, a3 = species

model = m.Model()
model.add_geometry_object(box)
model.add_geometry_object(hole)
for s in species:
    model.add_species(s)

model.add_release_site(m.ReleaseSite(
    name='rel_a0', complex=a0, region=box, concentration=1e-6, release_time=0))
model.add_release_site(m.ReleaseSite(
    name='rel_a1', complex=a1, region=box, concentration=1e-6, release_time=2e-6))
model.add_release_site(m.ReleaseSite(
    name='rel_a2', complex=a2, region=box, number_to_release=1000, release_time=2e-6))
model.add_release_site(m.ReleaseSite(
    name='rel_a3', complex=a3, region=box - hole, number_to_release=1000, release_time=2e-6))
model.add_release_site(m.ReleaseSite(
    name='remove_a2', complex=a2, region=box, number_to_release=-500, release_time=3e-6))

model.config.total_iterations = 4
model.config.seed = SEED
model.initialize()

out_dir = os.path.join('react_data', 'seed_' + str(SEED).zfill(5))
os.makedirs(out_dir, exist_ok=True)
summary = open(os.path.join(out_dir, 'release_summary.txt'), 'w')
summary.write('# iteration species molecules above_z_0.5_um in_hole\n')


def in_hole(p):
    return all(abs(c) < 0.2 for c in p)


def in_moved_cube(p):
    return abs(p[0]) <= 0.5 and abs(p[1]) <= 0.5 and -0.5 <= p[2] <= 1.5


# number of molecules, number above z = 0.5 um, number in the hole, per species
def summarize(iteration):
    res = {}
    for s in species:
        positions = [model.get_molecule(i).pos3d for i in model.get_molecule_ids(pattern=m.Complex(s.name))]
        assert all(in_moved_cube(p) for p in positions)
        res[s.name] = (
            len(positions),
            sum(1 for p in positions if p[2] > 0.5),
            sum(1 for p in positions if in_hole(p)))
        summary.write('%d %s %d %d %d\n' % ((iteration, s.name) + res[s.name]))
    return res


model.run_iterations(1)
r = summarize(1)
assert r['a0'][0] == 602 and r['a0'][1] == 0
assert r['a1'][0] == 0 and r['a2'][0] == 0 and r['a3'][0] == 0

# the top face moves up by 1 um
for i, v in enumerate(box.vertex_list):
    if v[2] > 0:
        model.add_vertex_move(box, i, [0, 0, 1.0])
model.apply_vertex_moves(randomize_order=False)

model.run_iterations(2)
r = summarize(3)
assert r['a0'][0] == 602 and r['a0'][1] == 0
assert r['a1'][0] == 1204
assert r['a2'][0] == 1000
assert r['a3'][0] == 1000 and r['a3'][2] == 0
for name in ['a1', 'a2', 'a3']:
    assert r[name][1] > 0, name + ' has no molecule in the part that the move added'
a2_above_before_removal = r['a2'][1]

model.run_iterations(1)
r = summarize(4)
assert r['a2'][0] == 500
assert 0 < r['a2'][1] < a2_above_before_removal, 'the removal took no molecule a2 from the part that the move added'

summary.close()
model.end_simulation()
