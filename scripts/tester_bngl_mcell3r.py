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
from test_utils import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error
from test_utils import log_test_error

UPDATE_REFERENCE=False

MCELL_BASE_ARGS = ['-seed', '1']
SEED_DIR = 'seed_00001'


class TesterBnglMcell3R(TesterBase):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterBnglMcell3R, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.bngl_to_data_model_script):
            fatal_error("Could not find bngl to data model conversion script '" + tool_paths.bngl_to_data_model_script + ".")

        if not os.path.exists(tool_paths.data_model_to_mdl_script):
            fatal_error("Could not find data model conversion script '" + tool_paths.data_model_to_mdl_script + ".")
            
        TesterBase.check_prerequisites(tool_paths)   


    def run_bngl_to_dm_conversion(self, bngl_file_name: str, extra_arg: str = None) -> None:
        # the conversion python script is considered a separate utility, 
        # we run it through bash 
        cmd = [ 
            self.tool_paths.python_binary, self.tool_paths.bngl_to_data_model_script, 
            bngl_file_name, 'data_model.json']
        if extra_arg:
            cmd.append(extra_arg)    
        log_name = self.test_name+'.bngl_to_dm.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name)
        if exit_code != 0:
            log_test_error(self.test_name, self.tester_name, "BGNL to mdl conversion failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_DM_TO_MDL_CONVERSION
        else:
            return PASSED

        
    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED
            
        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        mcell_args = MCELL_BASE_ARGS.copy()
        if self.mcell4_testing:
            mcell_args.append('-mcell4')

        res = self.run_bngl_to_dm_conversion(os.path.join(self.test_src_path, 'test.bngl'))
        if res != PASSED:
            return res
        
        res = self.run_dm_to_mdl_conversion(os.path.join(self.test_work_path, 'data_model.json'))
        if res != PASSED:
            return res
        res = self.change_viz_output_to_ascii()
        if res != PASSED:
            return res        
        
        res = self.run_mcell(mcell_args, os.path.join('..', self.test_work_path, MAIN_MDL_FILE))
        
        if self.is_todo_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec():
            return res
        
        res = self.check_reference_data(SEED_DIR, viz_ref_required=True)
        return res
