#!/usr/bin/env python3

import sys
import os
import array

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m



def read_cellblender_viz_output(file_name):
    # code based on cellblender/cellblender_mol_viz.py function mol_viz_file_read 
    mol_dict = {}
    
    with open(file_name, 'rb') as mol_file:

        # first 4 bytes must contain value '1'
        b = array.array("I")
        b.fromfile(mol_file, 1)
        ver = b[0]
        assert ver == 1 or ver == 2 
        
        while True:
            try:
                # ni = Initially, byte array of molecule name length.
                # Later, array of number of molecule positions in xyz
                # (essentially, the number of molecules multiplied by 3).
                # ns = Array of ascii character codes for molecule name.
                # s = String of molecule name.
                # mt = Surface molecule flag.
                
                if ver == 1:
                    ni = array.array("B")          # Create a binary byte ("B") array to read one byte
                else:
                    ni = array.array("I")          # Create a binary integer ("I") array to read 4 bytes
                
                ni.fromfile(mol_file, 1)       # Read one byte or uint which is the number of characters in the molecule name
                ns = array.array("B")          # Create another byte array to hold the molecule name
                ns.fromfile(mol_file, ni[0])   # Read ni bytes from the file
                mol_name_from_file = ns.tostring().decode()     # Decode bytes as ASCII into a string (s)
                
                
                mt = array.array("B")          # Create a byte array for the molecule type
                mt.fromfile(mol_file, 1)       # Read one byte for the molecule type
                ni = array.array("I")          # Re-use ni as an integer array to hold the number of molecules of this name in this frame
                ni.fromfile(mol_file, 1)       # Read the 4 byte integer value which is the number of molecules (v2) or 3 times the number of molecules (v1)
                
                if ver > 1:
                    num_mols = ni[0]
                    num_floats = 3*ni[0]
                    mol_ids = array.array("I")         
                    mol_ids.fromfile(mol_file, num_mols)
                else:
                    num_floats = ni[0]
                    mol_ids = None 
                
                mol_pos = array.array("f")     # Create a floating point array to hold the positions
                mol_orient = array.array("f")  # Create a floating point array to hold the orientations
                mol_pos.fromfile(mol_file, num_floats)  # Read all the positions which should be 3 floats per molecule
                if mt[0] == 1:                                        # If mt==1, it's a surface molecule
                    mol_orient.fromfile(mol_file, num_floats)              # Read all the surface molecule orientations
                
                mol_name = mol_name_from_file      # Construct name of blender molecule viz object
                
                mol_dict[mol_name] = [mt[0], mol_pos, mol_orient, mol_ids]     # Create a dictionary entry for this molecule containing a list of relevant data
            except EOFError:
                mol_file.close()
                break
        
    return mol_dict


# create main model object (empty)
model = m.Model()

model.load_bngl('model.bngl')

SEED = 0
prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene'

viz_output = m.VizOutput(
    mode = m.VizMode.CELLBLENDER_V1,
    output_files_prefix = prefix
)
model.add_viz_output(viz_output)

model.config.total_iterations = 1
   
# ---- initialization and execution ----

model.initialize()
model.run_iterations(1)
model.end_simulation()

# read cellbnder viz output 
mol_dict = read_cellblender_viz_output(prefix + '.cellbin.1.dat')

def assert_eq(a, b):
    assert abs(a - b) < 1e-6

def assert_eq_vec3(a, b):
    assert_eq(a.x, b.x)
    assert_eq(a.y, b.y)
    assert_eq(a.z, b.z)

# and compare it against a reference checked against ascii output
#  va@CP 0 0.311161 0.145214365 0.32167688 0 0 0
#  va@CP 1 -0.0498850037 -0.415475712 0.426996041 0 0 0
#  sb@PM 2 0.5 -0.0639481536 0.170722492 1 0 0
#  sb@PM 3 0.307013747 0.5 -0.174133457 -0 1 0 
# we cannot use model.get_molecule because binary viz data do not contain 
# molecule ids 
for species, data in mol_dict.items():
    if species == 'sb@PM':
        assert len(data) == 4
        assert data[0] == 1
        pos = data[1]
        assert_eq_vec3(
            m.Vec3(pos[0], pos[1], pos[2]),
            m.Vec3(0.5, -0.0639481536, 0.170722492)
        )
        assert_eq_vec3(
            m.Vec3(pos[3], pos[4], pos[5]),
            m.Vec3(0.307013747, 0.5, -0.174133457)
        )
        norms = data[2]
        assert_eq_vec3(
            m.Vec3(norms[0], norms[1], norms[2]),
            m.Vec3(1, 0, 0)
        )
        assert_eq_vec3(
            m.Vec3(norms[3], norms[4], norms[5]),
            m.Vec3(0, 1, 0)
        )
    elif species == 'va@CP':
        assert len(data) == 4
        assert data[0] == 0
        pos = data[1]
        assert_eq_vec3(
            m.Vec3(pos[0], pos[1], pos[2]),
            m.Vec3(0.311161, 0.145214365, 0.32167688)
        )
        assert_eq_vec3(
            m.Vec3(pos[3], pos[4], pos[5]),
            m.Vec3(-0.0498850037, -0.415475712, 0.426996041)
        )
    else:
        assert False


     
     
     
     
     
