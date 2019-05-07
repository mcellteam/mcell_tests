import os
import sys
import subprocess
import shutil


EPS = 1e-15
EXPECTED_NR_OF_VALUES = 7

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

    