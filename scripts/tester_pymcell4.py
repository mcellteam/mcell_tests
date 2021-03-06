"""
Copyright (C) 2019,2020 by
The Salk Institute for Biological Studies and
Pittsburgh Supercomputing Center, Carnegie Mellon University

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
"""

"""
Practically the same as tester_pymcell, however the prerequisites are different 
and the check cannot be easily parametrized. Quite probably it will evolve more 
in the future. 
"""

import os
import sys
import shutil
from typing import List, Dict

from test_settings import *
from tester_base import TesterBase
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False


class TesterPymcell4(TesterBase):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.pymcell4_lib):
            fatal_error("Could not find library '" + tool_paths.pymcell4_lib + ".")
        
    def update_reference(self) -> None:
        seed_dir = self.get_seed_dir()
        reference = os.path.join('..', self.test_src_path, REF_VIZ_OUTPUT_DIR, seed_dir)
        new_res = os.path.join(VIZ_OUTPUT_DIR, seed_dir)

        log("Updating reference " + reference + " with data from " + new_res + " (cwd:" + os.getcwd() + ")")
        
        # remove whole directory
        if os.path.exists(reference):
            log("Cleaning old data in " + reference + " (cwd:" + os.getcwd() + ")")
            shutil.rmtree(reference)
            
        shutil.copytree(new_res, reference)


    def run_pymcell4(self, test_dir:str, test_file='model.py', extra_args=[], seed=1, timeout_sec=MCELL_TIMEOUT) -> int:
        # we need to set the path to the build using MCELL_PATH system variable 
        # and the command will be executed as shell (on Linux and MacOS)
        # keep it separate like this so it is possibly just to copy the command on Linux and Mac
        if os.name != 'nt':
            cmdstr = 'export ' + MCELL_PATH_VARIABLE + '=' + self.tool_paths.mcell_path + ';'
            env = {}
        else:
            cmdstr = ''
            env = {MCELL_PATH_VARIABLE: self.tool_paths.mcell_path}
            
        cmdstr +=  self.tool_paths.python_binary + ' ' + os.path.join(test_dir, test_file) + ' '
        
        # seed set as argument to this method has higher priority
        if seed != 1:
            self.used_seed = seed
        elif self.extra_args.custom_seed_arg:
            self.used_seed = self.extra_args.custom_seed_arg
        else:
            self.used_seed = 1

        cmdstr += '-seed ' + str(self.used_seed) + ' ' 

        # mixing string and list arguments but it does not matter because all will be converted to a string
        cmd = [cmdstr]
        cmd += extra_args
        
        log_name = self.test_name + '_' + str(seed).zfill(5) + '.pymcell4.log'
        # run in work directory
        exit_code = run(cmd, shell=True, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=timeout_sec, extra_env=env)
        if (exit_code):
            self.log_test_error("Pymcell4 failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED
        
    def test(self) -> int:
            
        if self.should_be_skipped():
            return SKIPPED

        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        self.copy_all_extra_files_to_work_dir()
        
        res = self.run_pymcell4(test_dir=self.test_src_path)
        
        if self.is_todo_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec():
            return res
    
        if not UPDATE_REFERENCE:
            res = self.check_reference_data()
        else:
            self.update_reference()
        
        return res
