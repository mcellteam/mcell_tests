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
from tester_data_model_pymcell4 import TesterDataModelPymcell4
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

EXPORT_SCRIPT = 'export_to_data_model.py'

class TesterBnglDataModelPymcell4(TesterDataModelPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterBnglPymcell4, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterDataModelPymcell4.check_prerequisites(tool_paths)        

    def copy_exporter_and_test(self):
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, EXPORT_SCRIPT),
            self.test_work_path 
        )

        shutil.copy(
            os.path.join(self.test_src_path, 'test.bngl'),
            self.test_work_path 
        )
        
    def should_be_skipped_for_bngl_datamodel_pymcell4_test(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'skip_bngl_datamodel_pymcell4')):
            self.log_test_skip("SKIP BNGL_DATAMODEL_PYMCELL4")
            return True
        else:
            return False
        
    
    def test(self) -> int:
            
        if self.should_be_skipped_for_bngl_datamodel_pymcell4_test():
            return SKIPPED
            
        if self.should_be_skipped():
            return SKIPPED

        if self.is_known_fail():
            return SKIPPED
        
        if ARG_CHECKPOINTS in self.args:
            iters = self.load_checkpoint_iters()
            if not iters:
                return IGNORED        
        
        self.clean_and_create_work_dir()
        
        self.copy_exporter_and_test()
        
        # 1) export data model (run exporter.py)
        res = self.run_pymcell4(test_dir=self.test_work_path, test_file=EXPORT_SCRIPT)
        
        # 2) run data model to python converter w, w/o bngl
        if res == PASSED:
            extra_args = ['-t']
            if ARG_CONVERT_W_BNGL in self.args:
                extra_args += ['-b']
            if ARG_CHECKPOINTS in self.args:
                extra_args += ['-k', ','.join(iters)]                  
                
            res = self.run_dm_to_pymcell_conversion(
                os.path.join(self.test_work_path, 'data_model.json'), 
                extra_args=extra_args)
            
            # use specific error code
            if res != PASSED:
                res = FAILED_BNGL_TO_DM_CONVERSION
             
        # 3) run test (model.py)
        if res == PASSED:
            if ARG_CHECKPOINTS not in self.args:
                # single run
                res = self.run_pymcell4(test_dir=self.test_work_path)
            else:
                # run with checkpoints, run until run has finished
                # TODO: use seed argument 
                res = self.run_pymcell4(test_dir=self.test_work_path)
                while res == PASSED and \
                    not self.run_finished(os.path.join(self.test_work_path, 'reports/run_report_00001.txt')):
                    
                    res = self.run_pymcell4(test_dir=self.test_work_path)
        
        if self.is_todo_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec():
            return res
    
        res = self.check_reference_data(viz_ref_required=True)
        
        return res
