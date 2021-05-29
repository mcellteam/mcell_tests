import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

cplx = m.Complex('A(x~0)')
   
assert str(cplx) == 'A(x~0)'
   
assert "elementary_molecule_type=(ElementaryMoleculeType 'A'" in cplx.__str__(all_details=True) 


# species 
spec = m.Species('A', diffusion_constant_3d = 1e-6)

assert str(spec) == 'A'

assert "diffusion_constant_3d=1e-06" in spec.__str__(True) 

# geometry object
box = m.geometry_utils.create_box('box', 1)

#print(len(str(box)))
assert len(str(box)) < 150
   
#print(len(box.__str__(True)))
assert len(box.__str__(True)) > 150

