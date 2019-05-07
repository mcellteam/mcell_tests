import os
import sys
import subprocess
import shutil
from threading import Timer

import viz_output_diff

# all paths are relative to a which should be work
WORK_DIR = 'work'
VIZ_OUTPUT_DIR = os.path.join('4.', 'viz_data')
REF_VIZ_OUTPUT_DIR = 'ref_viz_data'
SEED_DIR = 'seed_00001'

TEST_DIR = os.path.join('..', 'tests')
MCELL_BINARY =os.path.join('..', '..', 'mcell', 'build', 'mcell')
MCELL_ARGS = ['-mcell4', '-seed', '1']
MAIN_MDL_FILE = 'Scene.main.mdl'

USE_SYSTEM_DIFF = False


def fatal_error(msg):
    print(msg)
    sys.exit(1)


def report_test_error(test_name, msg):
    print('ERROR: ' + test_name + ' - ' + msg)
    # terminate for now
    fatal_error('Ending after first error')


def report_test_success(test_name):
    print('PASS : ' + test_name)
    

def print_file(file_name):
    with open(file_name, "r") as fin:
        for line in fin:
            print(line)
            

def kill_proc(proc, f):
    proc.kill()
    f.write("Terminated after timeout")
    

def run(cmd, cwd=os.getcwd(), fout_name="", append_path_to_output=False, print_redirected_output=False, timeout_sec=30, verbose=False):
    if verbose:
        print("    Executing: '" + str.join(" ", cmd) + "' " + str(cmd))

    if append_path_to_output:
        full_fout_path = os.path.join(cwd, fout_name)
    else:
        full_fout_path = fout_name

    with open(full_fout_path, "w") as f:
        f.write("cwd: " + cwd + "\n")
        f.write(str.join(" ", cmd) + "\n")  # first item is the command being executed

        proc = subprocess.Popen(cmd, shell=False, cwd=cwd, stdout=f, stderr=subprocess.STDOUT)
        timer = Timer(timeout_sec, kill_proc, [proc, f])
        try:
            timer.start()
            exit_code = proc.wait()
        finally:
            timer.cancel()

    if (print_redirected_output):
        print_file(full_fout_path)

    return exit_code


def check_prerequisites(): 
    if not os.path.exists(MCELL_BINARY):
      fatal_error("Could not find executable '" + MCELL_BINARY + ".") 
  
  
def get_test_dirs():
    res = []
    files = os.listdir(os.path.abspath(TEST_DIR))
    for name in files:
        name_w_dir = os.path.join(TEST_DIR, name)
        if os.path.isdir(name_w_dir):
            res.append(name_w_dir)
    return res


def run_mcell(test_name, test_dir):
    cmd = [ os.path.join('..', MCELL_BINARY) ]
    cmd += MCELL_ARGS
    cmd += [ os.path.join('..', test_dir, MAIN_MDL_FILE) ]
    log_name = test_name+'.mcell.log'
    exit_code = run(cmd, cwd=os.getcwd(),  fout_name=log_name)
    if (exit_code):
        report_test_error(test_name, "MCell failed, see '" + os.path.join(test_name, log_name) + "'.")


def check_viz_output(test_name, test_dir):

    if USE_SYSTEM_DIFF:
        # for now, lets' just use diff -r
        # better check later
        cmd = [ 'diff', '-r', VIZ_OUTPUT_DIR, os.path.join('..', test_dir, REF_VIZ_OUTPUT_DIR) ]    
        log_name = test_name+'.viz_diff.log'
        exit_code = run(cmd, cwd=os.getcwd(), fout_name=log_name)
        if (exit_code):
            report_test_error(test_name, "Diff failed, see '" + os.path.join(test_name, log_name) + "'.")
        else: 
            report_test_success(test_name)
    else:
        viz_output_diff.compare_viz_output_directory(
            os.path.join('..', test_dir, REF_VIZ_OUTPUT_DIR, SEED_DIR), 
            os.path.join(VIZ_OUTPUT_DIR, SEED_DIR))
        report_test_success(test_name)
        

def update_ref_viz_output(test_name, test_dir):
    ref_dir = os.path.join('..', test_dir, REF_VIZ_OUTPUT_DIR)
    shutil.rmtree(ref_dir)
    shutil.copytree(VIZ_OUTPUT_DIR, ref_dir)
    

def run_single_test(test_dir, update_reference_data):
    test_name = os.path.basename(test_dir)
    if os.path.exists(test_name):
        shutil.rmtree(test_name)
    os.mkdir(test_name)
    os.chdir(test_name)
    
    run_mcell(test_name, test_dir)
    
    if not update_reference_data:
        check_viz_output(test_name, test_dir)
    else:
        update_ref_viz_output(test_name, test_dir)

    os.chdir('..')
    

def run_tests(test_code, update_reference_data):
    test_dirs = get_test_dirs()
    test_dirs.sort()
    print("Tests: " + str(test_dirs))
    work_dir = os.getcwd()
    for dir in test_dirs:
        if not test_code or test_code in dir:
            print("Testing " + dir)
            run_single_test(dir, update_reference_data)
            os.chdir(work_dir)  # just to be sure, let's fix cwd
    

def main():
    check_prerequisites()
    
    update_reference_data = False
    test_code = ''
    if len(sys.argv) == 2:
        if sys.argv[1] == 'update':
            print('Update is not supported yet')
            sys.exit(1)
            update_reference_data = True
        else:
            test_code = sys.argv[1]
        
    run_tests(test_code, update_reference_data)


if __name__ == '__main__':
    main()
    

