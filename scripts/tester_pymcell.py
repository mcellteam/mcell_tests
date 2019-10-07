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

from test_settings import *
from tester_base import TesterBase
from test_utils import ToolPaths, report_test_error, report_test_success

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False

SEED_DIR = 'seed_0001'


class TesterPymcell(TesterBase):
    def __init___(self, test_dir: str, tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, tool_paths)
    
    def check_prerequisites(self) -> None:
        if not os.path.exists(self.tool_paths.pymcell_module):
            fatal_error("Could not find module '" + self.tool_paths.pymcell_module + ".")
        
    def update_reference(self) -> None:
        reference = os.path.join('..', self.test_src_path, REF_VIZ_OUTPUT_DIR, SEED_DIR)
        new_res = os.path.join(VIZ_OUTPUT_DIR, SEED_DIR)

        log("Updating reference " + reference + " with data from " + new_res + " (cwd:" + os.getcwd() + ")")
        
        # remove whole directory
        if os.path.exists(reference):
            log("Cleaning old data in " + reference + " (cwd:" + os.getcwd() + ")")
            shutil.rmtree(reference)
            
        shutil.copytree(new_res, reference)

    def run_pymcell(self) -> int:
        # we need to set the path to the build using MCELL_DIR system variable
        # and the command will be executed as shell
        cmdstr = 'export ' + MCELL_DIR_VARIABLE + '=' + self.tool_paths.mcell_dir_path + ';'
        cmdstr +=  PYTHON_BINARY + ' ' + os.path.join(self.test_src_path, self.test_name + '.py')
        cmd = [ cmdstr ]
        
        log_name = self.test_name+'.pymcell.log'
        exit_code = run(cmd, shell=True, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            report_test_error(self.test_name, "Pymcell failed, see '" + os.path.join(self.test_name, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED

    def test(self) -> int:
        self.check_prerequisites()

        if self.should_be_skipped():
            return SKIPPED

        self.clean_and_create_work_dir()
        
        res = self.run_pymcell()
        if res != PASSED and not self.expected_wrong_ec():
            return res
    
        if not UPDATE_REFERENCE:
            res = self.check_reference_data(SEED_DIR)
        else:
            self.update_reference()
        
        return res
