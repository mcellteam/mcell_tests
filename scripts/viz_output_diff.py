import os
import sys
import subprocess
import shutil
from utils import run
from utils import print_file

EPS = 1e-15
EXPECTED_NR_OF_VALUES = 7

USE_FDIFF = True

FDIFF = 'fdiff' 
FDIFF_DIR = os.path.join('..', '..', 'scripts', 'fdiff')

class LineInfo:
    def __init__(self):
        self.name = ''
        self.values = []

    # returns '' is the values are the same
    # else it returns an error message
    def is_equal(self, a, eps):
        if self.name != a.name:
            return 'Names differ: ' + self.name + ' vs. ' + a.name
        if len(self.values) != len(a.values):
            return 'Number of values differ: ' + len(self.values) + ' vs. ' + len(a.values)
        
        for i in range(0, len(self.values)):
            if abs(self.values[i] - a.values[i]) >= eps:
                return 'Value with index ' + str(i) + ' differs: ' + str(self.values[i]) + ' vs. ' + str(a.values[i])

        return ''


# for now terminates if there is an error
def read_viz_output_line(fin):
    line = fin.readline()
    res = LineInfo()
    if not line:
        return res
    
    # TODO: some tolerance
    items = line.split(' ')
    
    if len(items) != EXPECTED_NR_OF_VALUES + 1:
        print('Invalid line ' + line)
        sys.exit(1)
    
    res.name = items[0]
    for i in range(1, len(items)):
        res.values.append(float(items[i]))
    
    return res


# return True if two files are identical while counting with floating point tolerance
def compare_viz_output_files(fname_ref, fname_new):
    # print('Comparing: ' + fname_ref + ' and ' + fname_new)
    if USE_FDIFF:
        fdiff = os.path.join(FDIFF_DIR, FDIFF)
        if not os.path.exists(fdiff):
            make_ec = run(
                ['make'], 
                cwd=os.path.abspath(FDIFF_DIR),
                verbose=True, 
                fout_name='make.log', 
                print_redirected_output=True
            )
            if make_ec != 0:
                print('Could not builf fdiff, terminating')
                sys.exit(1) 
            
        ec = run(
            [os.path.join(FDIFF_DIR, FDIFF), fname_ref, fname_new], 
            cwd=os.getcwd(),
            verbose=False, 
            fout_name='diff.log', 
            print_redirected_output=False
        )
        if ec != 0:
            print_file('diff.log')
            return False
        else:
            return True
    else:
        with open(fname_ref, "r") as fref:
            with open(fname_new, "r") as fnew:
                
                line = 0
                end = False
                while not end:
                    info_ref = read_viz_output_line(fref)
                    info_new = read_viz_output_line(fnew)
                    
                    line += 1
                    
                    if info_ref.values == [] and info_new.values == []:
                        return True
                    
                    if info_ref.values == [] or info_new.values == []:
                        print('Files ' + fname_ref + ' and ' + fname_new + ' have different count of lines')
                        return False
                    
                    diff_msg = info_ref.is_equal(info_new, EPS)
        
                    if diff_msg:
                        print('Difference between ' + fname_ref + ' and ' + fname_new + ': ' +  diff_msg)
                        return False
                
                
def compare_viz_output_directory(dir_ref, dir_new):
    files_ref = os.listdir(os.path.abspath(dir_ref))
    # print("***" + str(files_ref))
    for fname in files_ref:
        if '.dat' in fname:
            fname_ref = os.path.join(dir_ref, fname)
            fname_new = os.path.join(dir_new, fname)
            res = compare_viz_output_files(fname_ref, fname_new)
            if not res:
                print('Comparison failed.')
                sys.exit(1)

    