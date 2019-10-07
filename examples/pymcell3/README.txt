This directory contains pyMCell examples.

Only the pymcell directories are being tested.
 
All the source data are present here, those usually are:
- .py file that uses pymcell
- .json file exported from blender
- generated .mdl files of a reference model  


Reference output and scripts for testing will be added in the future. 

To run the pymcell tests, a system variable MCELL_DIR must be set e.g. like this:

export MCELL_DIR=`pwd`/../../../../mcell/build

Also, mcell must be built, for this see - mcell/README.md section "Building MCell Executable from Source",
for debug build, run this command in the mcell/build directory:

cmake .. -DCMAKE_BUILD_TYPE=Debug; make

---

0000_1_molecule_type_diffuse:

This is a simple example that shows basic pymcell functionality.
To verify that the pyMCell model produces the same result as the MDL MCell model, 
one can first run mcell directly:

cd 0000_1_molecule_type_diffuse/mdl/
$MCELL_DIR/mcell -seed 1 Scene.main.mdl

and then 

python 0000_1_molecule_type_diffuse.py

---

1000_2_molecule_types_diffuse_in_box_w_plane

This is a basic example with a box where in the upper half and also in the lower half, some 
molecules are released and diffused.
One can try out the model in Blender using:

File -> Import -> Data Model with Geometry JSON, there select file

examples_pymcell/1000_2_molecule_types_diffuse_in_box_w_plane/json/1000_2_molecule_types_diffuse_in_box_w_plane.json

after that:
Run Simulation
Reload Visualization Data
zoom into the cube and then play the animation - one should see red and green molecules being diffused


The next steps can be:
- extend pyMCell interface to get number of collisions with the plane inside of the box
- extend pyMCell interface to somehow modify the plane (e.g. position or to split into multiple triangles so that the chnges can be smoother)


One can also run mcell in the 1000_2_molecule_types_diffuse_in_box_w_plane/mdl directory:

$MCELL_DIR/mcell -seed 1 Scene.main.mdl

The configuration in Scene.rxn_output.mdl sets to capture hits of the plane object and 
the hits are reported in 1000_2_molecule_types_diffuse_in_box_w_plane/mdl/react_data/seed_00001/a.Plane.hits.dat like this:

iteration time  precise time      x            y            z  direction 
1.1e-05         1.11392700201e-05 0.0185766909 0.0163096248 0  1

x, y, z is the position where the plane was hit, direction 1 menas that the plane was hit from the top
