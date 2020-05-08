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
from tester_base import TesterBase
from test_utils import ToolPaths, log_test_error, log_test_success, replace_in_file

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE = False

MCELL_BASE_ARGS = ['-seed', '1']
SEED_DIR = 'seed_00001'


class TesterDataModelConverter(TesterBase):
    def __init___(self, test_src_path: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_src_path, args, tool_paths)
        
    @staticmethod
    def check_prerequisites(tool_paths) -> None:
        if not os.path.exists(tool_paths.data_model_to_mdl_script):
            fatal_error("Could not find data model conversion script '" + tool_paths.data_model_to_mdl_script + ".")
            
        TesterBase.check_prerequisites(tool_paths)

    
    def run_mdl_to_dm_conversion(self, mcell_args: List[str], main_mdl_file: str):
        cmd = [ self.tool_paths.mcell_binary ]
        cmd += mcell_args
        cmd += [ main_mdl_file ]
        cmd += self.extra_args.mcell_args
        cmd += [ '-mdl2datamodel4' ]
        
        log_name = self.test_name+'.mcell.log'
        exit_code = run(cmd, cwd=self.test_work_path, verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            log_test_error(self.test_name, "MCell datamodel conversion failed, see '" + os.path.join(self.test_name, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED


    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED
            
        if self.is_known_fail():
            return KNOWN_FAIL
        
        self.clean_and_create_work_dir()
        
        res = self.run_mdl_to_dm_conversion(MCELL_BASE_ARGS, os.path.join(self.test_src_path, MAIN_MDL_FILE))

        if res == PASSED:
            res = self.run_dm_to_mdl_conversion(os.path.join(self.test_work_path, 'datamodel.json'))
            
        if res == PASSED:
            res = self.change_viz_output_to_ascii()
            
        if res == PASSED:
            res = self.run_mcell(MCELL_BASE_ARGS, os.path.join(self.test_work_path, MAIN_MDL_FILE))
        
        if self.is_todo_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec() and not self.is_todo_test():
            return res
        
        return res
