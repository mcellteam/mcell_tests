import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from scipy.signal import find_peaks


SKIPS = [54]

def load_dat_file(file):
    obs_name = os.path.splitext(os.path.basename(file))[0]
    df = pd.read_csv(file, sep=' ', index_col='time', names=['time', obs_name])
    return df, obs_name
    
    
def get_peaks_for_single_obs(df, obs_name, file):
    peaks, _ = find_peaks(df[obs_name], width=int(len(df)/25))
    
    #if len(peaks) == 3 or len(peaks) == 4:
    
    if len(peaks) == 1:
        print("Warnign: only one peak found, skipping (" + file + ")")
        return 0, 0, True
        
    times = [ df.index.values[p] for p in peaks ]
    
    if len(peaks) != 2:
        #print(peaks)
        p0 = times[0]
        
        
        if obs_name == 'A':
            min_time = 16
        else: 
            min_time = 21
        
        p1 = None
        for t in times:
            if t > min_time:
                p1 = t
                break 
            
         
        print("Warnign: multiple peaks, selecting " + str(p0) + " and " + str(p1) + 
              " from " + str(times) + "         (" + file + ")")
    else:
        p0 = times[0]
        p1 = times[-1]
    
    return p0, p1, False
        
        
def get_all_peaks(dir):
    res = pd.DataFrame(columns = ['seed', 'A_first', 'A_second', 'R_first', 'R_second'])
    
    seed_dirs = os.listdir(dir)
    for seed_dir in sorted(seed_dirs):
        if not seed_dir.startswith('seed_'):
            continue
        
        seed = int(seed_dir[len('seed_'):])
        
        if seed in SKIPS: # some data do nto have the correct number of peaks
            continue
        
        new_row = [seed, 0.0, 0.0, 0.0, 0.0]
        skip_row = False
        
        file_list = os.listdir(os.path.join(dir, seed_dir))
        for file in file_list:
            file_path = os.path.join(dir, seed_dir, file)
            if os.path.isfile(file_path) and file.endswith('.dat'):    
                df, obs_name = load_dat_file(file_path)
                if obs_name == 'AR':
                    continue
                
                p0, p1, skip = get_peaks_for_single_obs(df, obs_name, file_path)
                
                skip_row = skip_row or skip 
                if obs_name == 'A':
                    new_row[1] = p0
                    new_row[2] = p1
                else:
                    new_row[3] = p0
                    new_row[4] = p1
        
        a_series = pd.Series(new_row, index = res.columns)
        res = res.append(a_series, ignore_index=True)
                
    return res

    
def print_peaks(df):
    
    #df['wavelength'] = df['A_second'] - df['A_first']    
    #df['lag_time'] = df['A_second'] - df['A_first']
        
    for col in df.columns:
        if col == 'seed':
            continue
        
        print(col + ": " + str(df[col].mean()) + " +- " + str(df[col].std()))    
        
    
if __name__ == '__main__':
    df = get_all_peaks(sys.argv[1])
    print_peaks(df)
    
    