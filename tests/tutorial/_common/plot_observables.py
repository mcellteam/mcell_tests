import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import glob

def load_dat_files(dat_dir):
    counts = {}
    
    res = pd.DataFrame
    
    # read all .dat files
    dat_files = sorted(glob.glob(os.path.join(dat_dir, "*.dat"))) 
    for file in dat_files:
        observable = os.path.splitext(os.path.basename(file))[0]
        df = pd.read_csv(file, sep=' ', index_col='time', names=['time', observable])

        # use the first data frame as basis and the join with new observables 
        # to create a single data frame        
        if res.empty:
            res = df
        else:
            res = res.join(df)

    return res


def main():
    if len(sys.argv) != 2:
        sys.exit("Expecting exactly one argument that is the path to directory with .dat files.")
    
    # load all .dat files in directory passed as the first argument
    dat_dir = sys.argv[1]
    if not os.path.exists(dat_dir):
        sys.exit("Directory " + dat_dir + " does not exist.")
    
    
    df = load_dat_files(dat_dir)
    
    df.plot(kind='line')
    plt.show()


if __name__ == '__main__':
    main()
    
    