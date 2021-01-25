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
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


class TesterPython(TesterBase):
    def __init___(self, test_src_path: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_src_path, args, tool_paths)
        
    @staticmethod
    def check_prerequisites(tool_paths) -> None:
        if not os.path.exists(tool_paths.python_binary) and not os.path.exists(shutil.which(tool_paths.python_binary)):
            fatal_error("Could not find Python binary executable '" + tool_paths.python_binary + "'.")
            
        TesterBase.check_prerequisites(tool_paths)
        
        
    def run_python_test(self) -> int:
        cmdstr =  self.tool_paths.python_binary + ' ' + os.path.join(self.test_src_path, self.test_name + '.py')
        cmd = [ cmdstr ]
        
        log_name = self.test_name+'.log'
        exit_code = run(cmd, shell=True, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            self.log_test_error("Python test failed, see '" + os.path.join(self.test_name, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED
        
                
    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED
            
        if self.is_known_fail():
            return KNOWN_FAIL
        
        self.clean_and_create_work_dir()
        
        res = self.run_python_test()
        
        if res != PASSED and not self.expected_wrong_ec():
            return res

        return res
