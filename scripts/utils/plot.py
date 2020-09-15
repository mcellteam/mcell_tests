
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def get_mcell_observables_counts(dir):
    counts = {}
    seed_dirs = os.listdir(dir)
    
    for seed_dir in seed_dirs:
        if not seed_dir.startswith('seed_'):
            continue
        
        file_list = os.listdir(os.path.join(dir, seed_dir))
        for file in file_list:
            file_path = os.path.join(dir, seed_dir, file)
            if os.path.isfile(file_path) and file.endswith('.dat'):
                observable = os.path.splitext(file)[0]
                if observable.endswith('_MDLString'):
                    observable = observable[:-len('_MDLString')]
                    
                with open(file_path, 'r') as f:
                    for line in f:
                        if line:
                            time_count = line.split()
                            time = float(time_count[0])
                            cnt = float(time_count[1])
                
                            if observable not in counts:
                                counts[observable] = {}
                                
                            if time not in counts[observable]:
                                counts[observable][time] = []
                            
                            counts[observable][time].append(cnt)
            
    return counts 


def get_bng_observables_counts(file, counts):
    if not os.path.exists(file):
        print("Expected file " + file + " not found, skipping it")
        return
     
    with open(file, 'r') as f:
        first_line = f.readline()
        observables = first_line.split()[1:]
        for line in f:
            if line:
                line_counts = line.split() # no leading '#'
            
                assert len(observables) == len(line_counts)
                time = float(line_counts[0])
                for i in range(1, len(observables)):
                    observable = observables[i]
                    cnt = float(line_counts[i])
                    
                    if observable not in counts:
                        counts[observable] = {}
                        
                    if time not in counts[observable]:
                        counts[observable][time] = []
                    
                    counts[observable][time].append(cnt)
                
                
def get_nfsim_observables_counts(dir):
    counts = {}
    nf_dirs = os.listdir(dir)
    
    for nf_dir in nf_dirs:
        full_dir = os.path.join(dir, nf_dir)
        if not nf_dir.startswith('nf_') or not os.path.isdir(full_dir):
            continue
        get_bng_observables_counts(os.path.join(full_dir, 'test.gdat'), counts)
            
    return counts 



mcell3_dir = 'react_data'
mcell4_dir = 'react_data4'
bng_dir = '.'
if len(sys.argv) == 4:
    mcell3_dir = sys.argv[1]
    mcell4_dir = sys.argv[2]
    bng_dir = sys.argv[3]

counts = []
counts.append(get_mcell_observables_counts(mcell3_dir))
counts.append(get_mcell_observables_counts(mcell4_dir))

# may be empty
counts.append(get_nfsim_observables_counts(bng_dir))

assert counts[0].keys() == counts[1].keys()
assert not counts[2] or counts[0].keys() == counts[2].keys()

names = ['MCell3R', 'MCell4', 'BNG']
clrs = ['b', 'g', 'r'] 
    
obs_i = 0
for obs in sorted(counts[0]): 
    
    fig,ax = plt.subplots()
    ax.set_title(obs)
    
    for i in range(len(counts)):
        if not counts[i]:
            print("Data for " + names[i] + " were not loaded.")
            continue
        times = []
        means = []
        stds = []
        
        for time in sorted(counts[i][obs]):
            #print(obs + ' ' + str(time))
            times.append(time)
            vals = np.array(counts[i][obs][time])
            means.append(vals.mean())
            stds.append(vals.std())
        
        ax.plot(times, means, label=obs + "1", c=clrs[i])
        ax.fill_between(
            times, 
            np.array(means)-np.array(stds), np.array(means)+np.array(stds),
            alpha=0.3, facecolor=clrs[i])


    plt.legend(names)
    
    plt.savefig(obs + '.png', dpi=1200)
    plt.close(fig)
