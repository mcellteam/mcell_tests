"""
Copyright (C) 2020 by
The Salk Institute for Biological Studies and
Pittsburgh Supercomputing Center, Carnegie Mellon University

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
"""

"""
This module contains functions to check tests in tests_mdl.
"""

import os
import sys
import shutil
from typing import List, Dict

from test_settings import *
from tester_bngl_pymcell4 import TesterBnglPymcell4
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

BNGL_EXPORT_SCRIPT = 'export_to_bngl.py'

class TesterBnglPymcell4Export(TesterBnglPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterBnglPymcell4, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterBnglPymcell4.check_prerequisites(tool_paths)        

    def copy_pymcell4_bngl_export_script(self):
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'export_to_bngl.py'),
            self.test_work_path 
        )
        
    
    def should_be_skipped_for_bngl_export(self):
        if os.path.exists(os.path.join(self.test_src_path, 'skip_bngl_export')):
            self.log_test_skip()
            return True
        else:
            return False
    
    def test(self) -> int:
            
        if self.should_be_skipped():
            return SKIPPED

        if self.is_known_fail():
            return SKIPPED

        if self.should_be_skipped_for_bngl_export():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        self.copy_pymcell4_runner_and_test()
        self.copy_pymcell4_bngl_export_script()
        
        # 1) export
        res = self.run_pymcell4(test_dir=self.test_work_path, test_file=BNGL_EXPORT_SCRIPT)
        if res != PASSED:
            if self.is_todo_test():
                return TODO_TEST
            else:
                return res
        
        # 2) run
        res = self.run_pymcell4(test_dir=self.test_work_path, extra_args=['-bngl', 'exported.bngl'])
        
        if self.is_todo_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec():
            return res
    
        # we need to use high tolerance because we are losing a lot of precision when recomputing volumes
        res = self.check_reference_data(viz_ref_required=True)
        
        return res
