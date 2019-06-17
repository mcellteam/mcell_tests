import os
import sys
import subprocess
import shutil
from threading import Timer
          

def kill_proc(proc, f):
    proc.kill()
    f.write("Terminated after timeout")

    
def print_file(file_name):
    with open(file_name, "r") as fin:
        for line in fin:
            print(line)
  

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
