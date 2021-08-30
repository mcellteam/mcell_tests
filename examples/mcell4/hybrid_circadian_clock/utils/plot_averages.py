#!/usr/bin/env python

"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to [http://unlicense.org] 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from io import StringIO


def load_gdat(file):
    wholefile = open(file).read()
    df = pd.read_csv(StringIO(wholefile[1:]), index_col=0, skipinitialspace=True, delim_whitespace=True)
    return df

def load_csv(file):
    df = pd.read_csv(file)
    df = df.set_index('time')
    return df

def main():
    if len(sys.argv) != 2:
        sys.exit("Expecting exactly one argument that is the .gdat " 
                 "file and optionally comma-separated column indices.")
    
    
    
    # load all .gdat and .csv files in directory passed as the first argument
    data = {}
    
    file_list = os.listdir(sys.argv[1])
    for file in file_list:
        file_path = os.path.join(sys.argv[1], file)
        if os.path.isfile(file_path):
            name_ext = os.path.splitext(file)
            if name_ext[1] == '.gdat':
                data[name_ext[0]] = load_gdat(file_path)
            elif name_ext[1] == '.csv':
                data[name_ext[0]] = load_csv(file_path)
            
    fig, ax = plt.subplots()
    legend = []
    for name,df in data.items():
        yA = df['A_mean']
        yR = df['R_mean']
        ax.plot(df.index, yR)
        ax.plot(df.index, yA)
        
        legend.append(name + ':A_mean')
        legend.append(name + ':R_mean')
    
    plt.legend(legend)
    plt.show()


if __name__ == '__main__':
    main()
    
    