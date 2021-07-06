import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

values = m.data_utils.load_dat_file(os.path.join(MODEL_PATH, 'input.dat'))

# easier to load with python...
ref_values = [  
    [0.004255319, 3418.29518129466],
    [0.012765957, 3427.96047213975],
    [0.015602837, 6693.53370549986],
    [0.017021277, 13255.8115760977],
    [0.021985816, 8179.34879300052],
    [0.026241135, 5618.60336686736],
    [0.030496454, 4703.00074695445],
    [0.036879433, 4095.3321690891],
    [0.042553191, 3805.45691080602],
    [0.05035461, 3596.51553498125],
    [0.063120567, 3486.52887569285],
    [0.080141844, 3457.12066816725],
    [0.109929078, 3437.65309176781],
    [0.143971631, 3437.65309176781],
    [1, 3437.65309176781],
]

for i in range(len(values)):
    assert len(values[i]) == 2
    assert values[i][0] == ref_values[i][0]
    assert values[i][1] == ref_values[i][1]
    
    