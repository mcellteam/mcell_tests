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
from tester_pymcell4 import TesterPymcell4
from tool_paths import ToolPaths
import data_output_diff

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

EXPORTED_BNGL = 'exported.bngl'

class TesterPymcell4ExportBng(TesterPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.pymcell4_lib):
            fatal_error("Could not find library '" + tool_paths.pymcell4_lib + ".")
        if not tool_paths.bng2pl_script:
            fatal_error("Path to bionetgen must be set using -n.")
        if not os.path.exists(tool_paths.bng2pl_script):
            fatal_error("Could not find script '" + tool_paths.bng2pl_script + ".")
        
    def run_bng(self):
        
        cmd = [ self.tool_paths.bng2pl_script, EXPORTED_BNGL ]
        
        log_name = self.test_name + '.bng2pl.log'
        
        exit_code = run(cmd, shell=True, cwd=self.test_work_path, verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        
        if exit_code != 0 and not self.ignore_bng_fail():
            self.log_test_error("BNG2.pl failed, see '" + os.path.join(dir, log_name) + "'.")
            return FAILED_BNG2PL
        else:
            return PASSED
        
    def test(self) -> int:
            
        if self.should_be_skipped():
            return SKIPPED

        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        self.copy_all_extra_files_to_work_dir()
        
        res = self.run_pymcell4(test_dir=self.test_src_path)

        if self.is_todo_test():
            return TODO_TEST

        if res != PASSED and not self.expected_wrong_ec():
            return res
        
        # this run generates file 'exported.bngl' that must be run with BNG
        res = self.run_bng()
        if res != PASSED and not self.expected_wrong_ec_bng():
            return res

        # check MCell4 reference    
        res = self.check_reference_data(True)
        if res != PASSED:
            return res
        
        # and BNG reference
        res = data_output_diff.compare_data_output_files(
            os.path.join(self.test_src_path, 'ref_exported.gdat'), 
            os.path.join(self.test_work_path, 'exported.gdat'), 
            True, '')
        
        return res
