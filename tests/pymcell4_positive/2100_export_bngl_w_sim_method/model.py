import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

model = m.Model()
model.load_bngl('test.bngl')
model.config.time_step = 1e-6
model.config.seed = 1
model.config.total_iterations = 100


model.initialize()

# note: export_to_bngl is tested with conversions, this is just foir the 
# sim methods
model.export_to_bngl("ode.bngl", m.BNGSimulationMethod.ODE)
model.export_to_bngl("nf.bngl", m.BNGSimulationMethod.NF)

model.end_simulation()

def file_contains(fname, text):
    with open(fname) as f:
        for line in f:
            if text in line:
                return True
            
    return False

assert file_contains("ode.bngl", "method=>\"ode\"")
assert file_contains("nf.bngl", "method=>\"nf\"")
    