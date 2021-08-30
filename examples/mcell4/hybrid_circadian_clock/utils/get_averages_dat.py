import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from scipy.signal import find_peaks

from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

from get_peaks import load_dat_file


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
                
                if observable not in counts:
                    index = 0
                else:
                    index = counts[observable].shape[1] - 1 
                
                col_name = 'count' + str(index)
                df = pd.read_csv(file_path, sep=' ', names=['time', col_name])

                if observable not in counts:
                    counts[observable] = df
                else:
                    # add new column
                    counts[observable][col_name] = df[col_name]
                
    return counts 

def get_averages(dir):
    dfA = pd.DataFrame()
    dfR = pd.DataFrame()
    
    counts = get_mcell_observables_counts(dir)
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
                    