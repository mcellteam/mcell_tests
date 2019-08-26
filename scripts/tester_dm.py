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
from test_utils import ToolPaths, report_test_error, report_test_success, replace_in_file

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False

MCELL_ARGS = ['-seed', '1']
SEED_DIR = 'seed_00001'


class TesterDm(TesterBase):
    def __init___(self, test_dir: str, tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, tool_paths)
    
    
    def check_prerequisites(self): 
        if not os.path.exists(self.tool_paths.mcell_binary):
            fatal_error("Could not find executable '" + self.tool_paths.mcell_binary + ".")
            
        if not os.path.exists(self.tool_paths.data_model_to_mdl_script):
            fatal_error("Could not find data model conversion script '" + self.tool_paths.data_model_to_mdl_script + ".")
        
         
    def run_dm_to_mdl_conversion(self):
        # the conversion python script is considered a separate utility, 
        # we run it through bash 
        cmd = [ 
            PYTHON_BINARY, self.tool_paths.data_model_to_mdl_script, 
            os.path.join(self.test_set_dir, self.test_name, self.test_name + '.json'), MAIN_MDL_FILE ]
        log_name = self.test_name+'.dm_to_mdl.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name)
        if exit_code != 0:
            report_test_error(self.test_name, "JSON to mdl conversion failed, see '" + os.path.join(self.test_name, log_name) + "'.")
            return FAILED_DM_TO_MDL_CONVERSION
        else:
            return PASSED
        
        
    def change_viz_output_to_ascii(self):
        fname = os.path.join(self.test_work_dir, 'Scene.viz_output.mdl')
        replace_in_file(fname, 'CELLBLENDER', 'ASCII')
        return PASSED
            

    def update_reference(self):
        assert False # TODO: copy only the last file...
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
        
        res = self.run_dm_to_mdl_conversion()
        if res != PASSED:
            return res
        
        res = self.change_viz_output_to_ascii()
        if res != PASSED:
            return res
         
        res = self.run_mcell(MCELL_ARGS, os.path.join(self.test_work_dir, MAIN_MDL_FILE))
    
        if not UPDATE_REFERENCE:
            if res == PASSED:
                res = self.check_viz_output(SEED_DIR)
            if res == PASSED:
                res = self.check_react_data_output(SEED_DIR)                
        else:
            if res != PASSED:
                fatal_error("Tried to update reference data but mcell execution failed!")
                
            self.update_reference()
    
        os.chdir('..')
        
        return res
