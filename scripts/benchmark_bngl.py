"""
Copyright (C) 2020 by
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
from benchmark_mdl import BenchmarkMdl
from test_utils import log_test_error
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


class BenchmarkBngl(BenchmarkMdl):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        BenchmarkMdl.check_prerequisites(tool_paths)        
        
    def run_pymcell_w_stats(self, log_name: str) -> int:

        cmdstr = 'export ' + MCELL_PATH_VARIABLE + '=' + self.tool_paths.mcell_path + '; '
        cmdstr += 'perf stat -e instructions:u '
        cmdstr +=  self.tool_paths.python_binary + ' ' + os.path.join(self.test_work_path, 'benchmark.py')
        cmd = [cmdstr]
        
        exit_code = run(cmd, shell=True, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            log_test_error(self.test_name, self.tester_name, "Pymcell4 failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED
        
    def copy_pymcell4_benchmark_runner_and_test(self):
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'benchmark.py'),
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
        
        self.copy_pymcell4_benchmark_runner_and_test()
        
        log_name = self.test_name+'.pymcell4.log'
        res = self.run_pymcell_w_stats(log_name)

        if self.is_todo_test():
            return TODO_TEST

        if res != PASSED:
            return res
        
        insns = self.get_insns_from_log(log_name)
        res = self.compare_insns_against_reference(insns)
        
        return res
