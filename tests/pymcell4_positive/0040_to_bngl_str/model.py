import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

C = m.ComponentType('C', ['0', '1', 'Z'])
N = m.ComponentType('N')
assert C.to_bngl_str() == 'C~0~1~Z'
assert N.to_bngl_str() == 'N'


C_inst = C.inst('1', 2)
C_inst2 = C.inst(1)
assert C_inst.to_bngl_str() == 'C~1!2'
assert C_inst2.to_bngl_str() == 'C~1'


CaM = m.ElementaryMoleculeType('CaM', [C, N], diffusion_constant_3d = 1e-6)
assert CaM.to_bngl_str() == 'CaM(C~0~1~Z,N)'


CaM_inst = CaM.inst([C.inst(0), N.inst(1)])
assert CaM_inst.to_bngl_str() == 'CaM(C~0,N~1)'


cplx_inst = m.Complex(
    elementary_molecules=[CaM.inst([C.inst(2, 1), N.inst(bond=2)]), CaM.inst([C.inst('Z', 1), N.inst(bond=2)])])
assert cplx_inst.to_bngl_str() == 'CaM(C~2!1,N!2).CaM(C~Z!1,N!2)'

cplx2 = m.Complex('Ca', compartment_name = 'CP')
assert cplx2.to_bngl_str() == 'Ca@CP'

cplx3 = m.Complex('A(a!1).B(b!1)', compartment_name = 'CP')
assert cplx3.to_bngl_str() == '@CP:A(a!1).B(b!1)'

cplx4 = m.Complex('A(a!1)@IN.B(b!1)')
assert cplx4.to_bngl_str() == 'A(a!1)@IN.B(b!1)'

CaMC0N1_species = m.Species(elementary_molecules = [ CaM.inst([C.inst(0), N.inst(1)]) ] )
assert CaMC0N1_species.to_bngl_str() == 'CaM(C~0,N~1)'


d = m.ComponentType('d') # no states  
l = m.ComponentType('l')
r = m.ComponentType('r')
Y286 = m.ComponentType('Y286', ['0','P'])
S306 = m.ComponentType('S306', ['0','P'])
cam = m.ComponentType('cam')

CaMKII = m.ElementaryMoleculeType(
    'CaMKII', 
    [d, r, l, Y286, S306],    
    diffusion_constant_3d = 1e-6
)

V = 0.125*1e-15 # um^3 -> liters
NA = 6.022e23/1e6
k_onCaMKII = 50/(NA*V) #1/uM 1/s 
k_offCaMKII = 60 #1/s 

rxn_rule = m.ReactionRule(
    name = "sixth rxn",
    rev_name = "sixth rxn rev",
    reactants=[
        m.Complex( 
            elementary_molecules=[ CaMKII.inst( [ l.inst(), r.inst(), Y286.inst('0'), cam.inst(bond=m.BOND_BOUND) ] ) ] 
        ),
        m.Complex( 
            elementary_molecules=[ CaMKII.inst( [ l.inst(), r.inst(), cam.inst(bond=m.BOND_BOUND) ] ) ]  
        )
    ], 
    products=[
        m.Complex( 
            elementary_molecules=[ CaMKII.inst( [ l.inst(1, bond=1), r.inst(), Y286.inst('0'), cam.inst(bond=m.BOND_BOUND) ] ), 
              CaMKII.inst( [ l.inst(), r.inst(bond=1), cam.inst(bond=m.BOND_BOUND) ] )
            ]
        )
    ],
    fwd_rate = k_onCaMKII,
    rev_rate = k_offCaMKII
)
assert rxn_rule.to_bngl_str() == 'CaMKII(l,r,Y286~0,cam!+) + CaMKII(l,r,cam!+) <-> CaMKII(l~1!1,r,Y286~0,cam!+).CaMKII(l,r!1,cam!+)'
