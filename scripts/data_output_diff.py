import os
import sys
import test
from test_settings import *

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', '..', 'mcell_tools', 'scripts'))
from utils import *

EPS = 1e-15
EXPECTED_NR_OF_VALUES = 7

FDIFF = 'fdiff' + EXE_EXT
DIFF = 'diff' + EXE_EXT

# FIXME: build it in 'work'
FDIFF_DIR = os.path.join(THIS_DIR, 'fdiff')

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
        log('Invalid line ' + line)
        sys.exit(1)
    
    res.name = items[0]
    for i in range(1, len(items)):
        res.values.append(float(items[i]))
    
    return res


def check_or_build_fdiff():
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
            fatal_error('Could not builf fdiff, terminating')
            
    return fdiff


# return True if two files are identical while counting with floating point tolerance
def compare_data_output_files(fname_ref, fname_new, exact, fdiff_args):
    
    if exact:
        cmd = [DIFF, fname_ref, fname_new] 
    else:
        diff_executable = check_or_build_fdiff()
        cmd = [diff_executable, fname_ref, fname_new]
        cmd += fdiff_args  # might be an empty list 
        
    ec = run(
        cmd, 
        cwd=os.getcwd(),
        verbose=False, 
        fout_name='diff.log', 
        print_redirected_output=False
    )
    if ec != 0:
        print_file('diff.log')
        return FAILED_DIFF
    else:
        return PASSED
                
                
def compare_data_output_directory(dir_ref, dir_new, exact=False, fdiff_args=[]):
    ref_dir = os.path.abspath(dir_ref)
    if not os.path.exists(ref_dir):
        log('Directory ' + ref_dir + ' does not exist')
        return FAILED_DIFF
        
    files_ref = os.listdir(ref_dir)
    
    for fname in files_ref:
        # FIXME: these error messages do not appear in the difff log
        fname_ref = os.path.join(dir_ref, fname)
        if not os.path.exists(fname_ref):
            log('File ' + fname_ref + ' does not exist')
            return FAILED_DIFF
        fname_new = os.path.join(dir_new, fname)
        if not os.path.exists(fname_new):
            log('File ' + fname_new + ' does not exist')
            return FAILED_DIFF
        
        res = compare_data_output_files(fname_ref, fname_new, exact, fdiff_args)
        if res != PASSED:
            log('Comparison failed.')
            return res
            
    return PASSED
    