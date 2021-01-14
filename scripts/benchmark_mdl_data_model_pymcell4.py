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
import re
from typing import List, Dict

from test_settings import *
from benchmark_bngl import BenchmarkBngl
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False

MCELL_BASE_ARGS = ['-seed', '1']

class BenchmarkMdlDataModelPymcell4(BenchmarkBngl):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        BenchmarkBngl.check_prerequisites(tool_paths)        
        
   
    def test(self) -> int:
        if self.should_be_skipped() and not self.tool_paths.opts.gen_benchmark_script:
            return SKIPPED
            
        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        self.copy_customization()

        
        extra_args = []
        if ARG_CONVERT_W_BNGL in self.args:
            extra_args = ['-b']   
            
        res = self.run_mdl_to_dm_conversion(MCELL_BASE_ARGS, os.path.join(self.test_src_path, MAIN_MDL_FILE))
        if res != PASSED:
            return res
            
        res = self.run_dm_to_pymcell_conversion(
            os.path.join(self.test_work_path, 'data_model.json'), 
            extra_args=extra_args)    
        if res != PASSED:
            return res
                    
        log_name = self.test_name+'.pymcell4.log'
        res = self.run_pymcell_w_stats('model.py', log_name)
        #print("Log: " + os.path.join(self.test_work_path, log_name))

        if self.is_todo_test():
            return TODO_TEST

        if res != PASSED:
            return res
        
        res = self.benchmark_report(log_name)
        
        return res
