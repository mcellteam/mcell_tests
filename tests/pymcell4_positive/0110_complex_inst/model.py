import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

C = m.Species(
    name = 'C(a)'
)

assert C.to_bngl_str() == 'C(a)'

# there was a bug where setting compartment name in instantiation changed 
# the compartment name for Species
inst = C.inst(compartment_name = 'EC')
assert inst.to_bngl_str() == 'C(a)@EC'

assert C.to_bngl_str() == 'C(a)'

inst = C.inst(compartment_name = 'EC')
inst.elementary_molecules[0].compartment_name = 'XX'
assert inst.to_bngl_str() == 'C(a)@XX'

assert C.to_bngl_str() == 'C(a)'
