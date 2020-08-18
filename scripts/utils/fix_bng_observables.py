import os
import sys

if len(sys.argv) != 2:
    print("Expecting input bngl file")
    sys.exit(1)
    
with open(sys.argv[1], 'r') as f:
    in_observables = False
    for line in f:
        if 'begin observables' in line:
            in_observables = True
            continue
        elif 'end observables' in line:
            in_observables = False
            continue
        
        if in_observables:
            items = line.split()
            if len(items) == 3:
                new_obs_name = items[2].replace('(', '').replace(')', '').replace('~', '').replace('!', '').replace('.', '').replace(',', '')
                print('    ' + items[0] + ' ' + new_obs_name + ' ' + items[2])