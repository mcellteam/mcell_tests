import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from scipy.signal import find_peaks

from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

from get_peaks import load_dat_file


def get_bng_observables_counts(file, counts):
    if not os.path.exists(file):
        print("Expected file " + file + " not found, skipping it")
        return
    
    with open(file, 'r') as f:
        first_line = f.readline()
        header = first_line.split()[1:]
    df = pd.read_csv(file, delim_whitespace=True, comment='#', names=header)
    return df
    

def process_nsfim_gdat_file(full_dir, counts):
    df = get_bng_observables_counts(os.path.join(full_dir, 'test.gdat'), counts)
    
    # transform into separate dataframes based on observable 
    for i in range(1, df.shape[1]):
        observable = df.columns[i] 
        if observable not in counts:
            col_name = 'count0'  
            # select time and the current observable
            counts[observable] = pd.DataFrame()           
            counts[observable]['time'] = df.iloc[:, 0]
            counts[observable][col_name] = df.iloc[:, i]
        else:
            col_name = 'count' + str(counts[observable].shape[1] - 1)            
            counts[observable][col_name] = df.iloc[:, i]             
                
                
def get_nfsim_observables_counts(dir):
    single_bng_run = False 
    counts = {}
    
    if not single_bng_run:
        nf_dirs = os.listdir(dir)
        
        for nf_dir in nf_dirs:
            full_dir = os.path.join(dir, nf_dir)
            if not nf_dir.startswith('nf_') or not os.path.isdir(full_dir):
                continue
            process_nsfim_gdat_file(full_dir, counts)
    else:
        process_nsfim_gdat_file(dir, counts)

    return counts 


def get_averages(dir):
    dfA = pd.DataFrame()
    dfR = pd.DataFrame()
    
    counts = get_nfsim_observables_counts(dir)
    print(counts)
                    
    df = pd.DataFrame()           
    df['time'] = counts['A'].iloc[:, 0]
    df['A_mean'] = counts['A'].iloc[:, 1:].mean(axis=1)                
    df['A_std'] = counts['A'].iloc[:, 1:].std(axis=1)
    df['R_mean'] = counts['R'].iloc[:, 1:].mean(axis=1)                
    df['R_std'] = counts['R'].iloc[:, 1:].std(axis=1)
    
    return df


def save_averages(df, outfile):
    df.to_csv(outfile)
                
if __name__ == '__main__':
    assert len(sys.argv) > 2, "dir and output file"
    df = get_averages(sys.argv[1])
    save_averages(df, sys.argv[2])
                    