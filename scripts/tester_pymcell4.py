"""
Copyright (C) 2019,2020 by
The Salk Institute for Biological Studies and
Pittsburgh Supercomputing Center, Carnegie Mellon University

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

For the complete terms of the GNU General Public License, please see this URL:
http://www.gnu.org/licenses/gpl-2.0.html
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
from test_utils import log_test_error
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False

SEED_DIR = 'seed_00001'


class TesterPymcell4(TesterBase):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.pymcell4_lib):
            fatal_error("Could not find library '" + tool_paths.pymcell4_lib + ".")
        
    def update_reference(self) -> None:
        reference = os.path.join('..', self.test_src_path, REF_VIZ_OUTPUT_DIR, SEED_DIR)
        new_res = os.path.join(VIZ_OUTPUT_DIR, SEED_DIR)

        log("Updating reference " + reference + " with data from " + new_res + " (cwd:" + os.getcwd() + ")")
        
        # remove whole directory
        if os.path.exists(reference):
            log("Cleaning old data in " + reference + " (cwd:" + os.getcwd() + ")")
            shutil.rmtree(reference)
            
        shutil.copytree(new_res, reference)


    def run_pymcell4(self, test_dir:str, test_file='model.py', extra_args=[], seed=1, timeout_sec=MCELL_TIMEOUT) -> int:
        # we need to set the path to the build using MCELL_PATH system variable
        # and the command will be executed as shell
        cmdstr = 'export ' + MCELL_PATH_VARIABLE + '=' + self.tool_paths.mcell_path + ';'
        cmdstr +=  self.tool_paths.python_binary + ' ' + os.path.join(test_dir, test_file)
        cmd = [ cmdstr, '-seed', str(seed) ]
        cmd += extra_args
        
        log_name = self.test_name + '_' + str(seed).zfill(5) + '.pymcell4.log'
        # run in wrk d
        exit_code = run(cmd, shell=True, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=timeout_sec)
        if (exit_code):
            log_test_error(self.test_name, self.tester_name, "Pymcell4 failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED
        
    def test(self) -> int:
            
        if self.should_be_skipped():
            return SKIPPED

        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        self.copy_all_bngl_files_to_work_dir()
        
        res = self.run_pymcell4(test_dir=self.test_src_path)
        
        if self.is_todo_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec():
            return res
    
        if not UPDATE_REFERENCE:
            res = self.check_reference_data(SEED_DIR)
        else:
            self.update_reference()
        
        return res
