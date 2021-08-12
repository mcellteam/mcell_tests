"""
Copyright (C) 2019 by
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
from tester_base import TesterBase
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False

MCELL_BASE_ARGS = ['-seed', '1']


class TesterMdl(TesterBase):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterBase.check_prerequisites(tool_paths)        
        
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

    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED
            
        if self.is_known_fail():
            return SKIPPED
        
        if not self.mcell4_testing and self.should_be_skipped_for_mcell3_test():   
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        mcell_args = MCELL_BASE_ARGS.copy()
        if self.mcell4_testing:
            mcell_args.append('-mcell4')
        
        res = self.run_mcell(mcell_args, os.path.join('..', self.test_src_path, MAIN_MDL_FILE))
        
        if self.is_todo_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec():
            return res
        
        if not UPDATE_REFERENCE:
            res = self.check_reference_data(viz_ref_required=True)
        else:
            self.update_reference()
        
        return res
