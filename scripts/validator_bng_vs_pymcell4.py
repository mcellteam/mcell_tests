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
import glob
from typing import List, Dict

from test_settings import *
from tester_bngl_pymcell4 import TesterBnglPymcell4
from test_utils import ToolPaths, log_test_error

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


NUM_MCELL_VALIDATION_RUNS = 10


class ValidatorBngVsPymcell4(TesterBnglPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.pymcell4_lib):
            fatal_error("Could not find library '" + tool_paths.pymcell4_lib + ".")
        # bionetgen path

    def copy_pymcell4_runner_and_test(self):
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'validation_model.py'),
            self.test_work_path 
        )
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'model.py'),
            self.test_work_path 
        )        

        shutil.copy(
            os.path.join(self.test_src_path, 'test.bngl'),
            self.test_work_path 
        )
        
        
    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED

        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        self.copy_pymcell4_runner_and_test()
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'validation_model.py'),
            self.test_work_path 
        )
                
        # run pymcell4 with different seeds
        # we simply count the resulting molecules with the viz output afterwards, no need to 
        # do anything with counting
        for i in range(0, NUM_MCELL_VALIDATION_RUNS) 
            res = self.run_pymcell(test_dir=self.test_src_path, test_file='validation_model.py', ['-seed', str(i)])
            if res != PASSED:
                log_test_error("Run of pymcell4 with seed " + str(i) + " in work dir " + self.test_src_path + " failed.")

        # run bng
        
        # process output
            
        if self.is_todo_test():
            return TODO_TEST
        
       
        return res
