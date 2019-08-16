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

import viz_output_diff
from test_settings import *
from tester_base import TesterBase
from test_utils import ToolPaths, report_test_error, report_test_success

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False

SEED_DIR = 'seed_00001'
MAIN_MDL_FILE = 'Scene.main.mdl'
MCELL_ARGS = ['-seed', '1']

if TEST_MCELL4:
    MCELL_ARGS.append('-mcell4')
    VIZ_OUTPUT_DIR = os.path.join('4.', 'viz_data')
    REF_VIZ_OUTPUT_DIR = 'ref_viz_data_4'
else:
    VIZ_OUTPUT_DIR = 'viz_data'
    REF_VIZ_OUTPUT_DIR = 'ref_viz_data_3'
    

class TesterMdl(TesterBase):
    def __init___(self, test_dir: str, tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, tool_paths)
    
    
    def check_prerequisites(self): 
        if not os.path.exists(self.tool_paths.mcell_binary):
            fatal_error("Could not find executable '" + self.tool_paths.mcell_binary + ".") 


    def check_viz_output(self):
        res = viz_output_diff.compare_viz_output_directory(
            os.path.join('..', self.test_dir, REF_VIZ_OUTPUT_DIR, SEED_DIR), 
            os.path.join(VIZ_OUTPUT_DIR, SEED_DIR))
        
        if res == PASSED:
            report_test_success(self.test_name) # fail is already reported in diff
        else:
            report_test_error(self.test_name, "Diff failed.")
        return res
        
    def update_reference(self):
        reference = os.path.join('..', self.test_dir, REF_VIZ_OUTPUT_DIR, SEED_DIR)
        new_res = os.path.join(VIZ_OUTPUT_DIR, SEED_DIR)

        log("Updating reference " + reference + " with data from " + new_res + " (cwd:" + os.getcwd() + ")")
        
        # remove whole directory
        if os.path.exists(reference):
            log("Cleaning old data in " + reference + " (cwd:" + os.getcwd() + ")")
            shutil.rmtree(reference)
            
        shutil.copytree(new_res, reference)
        

    def test(self):
        self.check_prerequisites()

        if os.path.exists(os.path.join(self.test_dir, 'skip')):
            log("SKIP : " + test_name)
            return SKIPPED

        self.clean_and_create_work_dir()
        
        res = self.run_mcell(MCELL_ARGS, MAIN_MDL_FILE)
    
        if not UPDATE_REFERENCE:
            if res == PASSED:
                res = self.check_viz_output()
        else:
            if res != PASSED:
                fatal_error("Tried to update reference data but mcell execution failed!")
                
            self.update_reference()
    
        os.chdir('..')
        
        return res
