
import pandas as pd
import sys
import os
from get_peaks import *
from io import StringIO


def load_gdat_file(file):
    wholefile = open(file).read()
    
    df = pd.read_csv(StringIO(wholefile[1:]), index_col=0, skipinitialspace=True, delim_whitespace=True)

    return df
   
def get_all_peaks_bngl(dir):
    res = pd.DataFrame(columns = ['seed', 'A_first', 'A_second', 'R_first', 'R_second'])
    
    num_skipped = 0
    
    seed_dirs = os.listdir(dir)
    for seed_dir in sorted(seed_dirs):
        if not seed_dir.startswith('nf_'):
            continue
        
        seed = int(seed_dir[len('nf_'):])
        
        new_row = [seed, 0.0, 0.0, 0.0, 0.0]
        skip_row = False
        
        file_path = os.path.join(dir, seed_dir, 'test.gdat')
        df = load_gdat_file(file_path)
        
        df_orig = df.copy()
        df = prepare_data(df, 'A')
        df = prepare_data(df, 'R')
        
        p0, p1, skip = get_peaks_for_single_obs(df, 'A', file_path)
        if skip:
            num_skipped += 1
            continue
        
        new_row[1] = p0
        new_row[2] = p1
        
        plot_peaks(df, df_orig, 'A', p0, p1, seed_dir)
                            
        p0, p1, skip = get_peaks_for_single_obs(df, 'R', file_path)
        if skip:
            num_skipped += 1
            continue

        new_row[3] = p0
        new_row[4] = p1
        
        plot_peaks(df, df_orig, 'R', p0, p1, seed_dir)
    
        a_series = pd.Series(new_row, index = res.columns)
        res = res.append(a_series, ignore_index=True)
                
    
    print("Skipped values: ", num_skipped)
    
    return res

if __name__ == '__main__':
    
    df = get_all_peaks_bngl(sys.argv[1])
    print_peaks(df)  