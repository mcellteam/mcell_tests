#!/usr/bin/env python3

import sys
import os

MCELL_DIR = os.environ.get('MCELL_DIR', '')
if MCELL_DIR:
    sys.path.append(os.path.join(MCELL_DIR, 'lib'))
else:
    print("Error: variable MCELL_DIR that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

par = m.bngl_utils.load_bngl_parameters('test.bngl')

a = 3.5
b = 2
c = a+b
d = a+b*c
e = (a+b)*c 
f = a-b*c
g = (a-b)*c
h = a**b*c
i = a**(b*c)
j = a*b/d
l = (a*b)/d
k = a+b*(c-d/e**f)
m = -a
n = +a
o = a**(b*c)-d/e*f+g
p = a**-5
q = -2**+2

assert par['a'] == a
assert par['b'] == b
assert par['c'] == c
assert par['d'] == d
assert par['e'] == e
assert par['f'] == f
assert par['g'] == g
assert par['h'] == h
assert par['i'] == i
assert par['j'] == j
assert par['k'] == k
assert par['l'] == l
assert par['m'] == m
assert par['n'] == n
assert par['o'] == o
assert par['p'] == p
assert par['q'] == q
