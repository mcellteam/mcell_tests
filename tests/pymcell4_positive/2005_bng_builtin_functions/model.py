#!/usr/bin/env python3

import sys
import os
import math

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

par = m.bngl_utils.load_bngl_parameters('test.bngl')

a = 0.6
b = -4.5
    
sqrt_a = math.sqrt(a)
exp_a = math.exp(a)
log_a = math.log(a)
log10_a = math.log10(a)
sin_a = math.sin(a)
cos_a = math.cos(a)
tan_a = math.tan(a)
asin_a = math.asin(a)
acos_a = math.acos(a)
atan_a = math.atan(a)

abs_a = abs(a)
abs_b = abs(b)
ceil_a = math.ceil(a)
ceil_b = math.ceil(b)
floor_a = math.floor(a)
floor_b = math.floor(b)

max_ab = max(a,b)
min_ab = min(a,b)

def eq(x, y):
    assert abs(x-y) < 1e-9

eq(par['a'], a)
eq(par['b'], b)
eq(par['sqrt_a'], sqrt_a)
eq(par['exp_a'], exp_a)
eq(par['log_a'], log_a)
eq(par['log10_a'], log10_a)
eq(par['sin_a'], sin_a)
eq(par['cos_a'], cos_a)
eq(par['tan_a'], tan_a)
eq(par['asin_a'], asin_a)
eq(par['acos_a'], acos_a)
eq(par['abs_a'], abs_a)
eq(par['abs_b'], abs_b)
eq(par['ceil_a'], ceil_a)
eq(par['ceil_b'], ceil_b)
eq(par['floor_a'], floor_a)
eq(par['floor_b'], floor_b)
eq(par['max_ab'], max_ab)
eq(par['min_ab'], min_ab)


