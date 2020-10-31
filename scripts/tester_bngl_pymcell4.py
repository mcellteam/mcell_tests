"""
Copyright (C) 2019 by
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
This module contains functions to check tests in tests_mdl.
"""

import os
import sys
import shutil
from typing import List, Dict

from test_settings import *
from tester_pymcell4 import TesterPymcell4
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


MCELL_BASE_ARGS = ['-seed', '1']


class TesterBnglPymcell4(TesterPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterBnglPymcell4, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterPymcell4.check_prerequisites(tool_paths)        

    def copy_pymcell4_runner_and_test(self):
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
        
        res = self.run_pymcell4(test_dir=self.test_work_path)
        
        if self.is_todo_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec():
            return res
    
        res = self.check_reference_data(viz_ref_required=True)
        
        return res
