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

UPDATE_REFERENCE = False

MCELL_BASE_ARGS = ['-seed', '1']
SEED_DIR = 'seed_00001'


class TesterDataModel(TesterBase):
    def __init___(self, test_src_path: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_src_path, args, tool_paths)

    @staticmethod
    def check_prerequisites(tool_paths) -> None:
        if not os.path.exists(tool_paths.data_model_to_mdl_script):
            fatal_error("Could not find data model conversion script '" + tool_paths.data_model_to_mdl_script + ".")
            
        TesterBase.check_prerequisites(tool_paths)

    def update_reference(self) -> None:
        viz_reference = os.path.join(self.test_src_path, get_ref_viz_data_dir(self.mcell4_testing), SEED_DIR)
        viz_res = os.path.join(self.test_work_path, get_viz_data_dir(self.mcell4_testing), SEED_DIR)

        if os.path.exists(viz_res):
            # remove whole directory
            if os.path.exists(viz_reference):
                log("Cleaning old data in " + viz_reference)
                shutil.rmtree(viz_reference)
                
            # copy the first and the last viz data file
            log("New reference from " + viz_res)
            files = os.listdir(viz_res)
            if not files:
                fatal_error("There are no reference data in " + viz_res)
                  
            files.sort()
    
            log("Updating reference " + viz_reference + " with data from " + viz_res)
            log("  File 1:" + files[0])
            log("  File 1:" + files[-1])
            
            if not os.path.exists(viz_reference):
                os.makedirs(viz_reference)
            shutil.copyfile(os.path.join(viz_res, files[0]), os.path.join(viz_reference, files[0]))
            shutil.copyfile(os.path.join(viz_res, files[-1]), os.path.join(viz_reference, files[-1]))
            
        # copy the whole react data files 
        react_reference = os.path.join(self.test_src_path, get_ref_react_data_dir(self.mcell4_testing), SEED_DIR)
        react_res = os.path.join(self.test_work_path, get_react_data_dir(self.mcell4_testing), SEED_DIR)
        
        if os.path.exists(react_res):
            # remove whole directory
            if os.path.exists(react_reference):
                log("Cleaning old data in " + react_reference)
                shutil.rmtree(react_reference)
    
            # and update all files
            log("Updating reference " + react_reference + " with data from " + react_res)
            shutil.copytree(react_res, react_reference)

        # copy the whole dyn_geom data files 
        dyn_geom_reference = os.path.join(self.test_src_path, REF_DYN_GEOM_DATA_DIR)
        dyn_geom_res = os.path.join(self.test_work_path, DYN_GEOM_DATA_DIR)
        
        if os.path.exists(dyn_geom_res):
            # remove whole directory
            if os.path.exists(dyn_geom_reference):
                log("Cleaning old data in " + dyn_geom_reference)
                shutil.rmtree(dyn_geom_reference)
    
            # and use every 100th file
            files = os.listdir(dyn_geom_res)
            if not files:
                fatal_error("There are no reference data in " + dyn_geom_res)
            files.sort()   
            
            if not os.path.exists(dyn_geom_reference):
                os.makedirs(dyn_geom_reference)
                
            log("Updating reference " + dyn_geom_reference + " with data from " + dyn_geom_res)
            for i in range(0, len(files), 50):
                log("Updating reference file '" + files[i] + '"')
                shutil.copyfile(os.path.join(dyn_geom_res, files[i]), os.path.join(dyn_geom_reference, files[i]))

        # and also check the .gdat files generated with mcellr mode
        mcellr_gdat_reference = os.path.join(self.test_src_path, REF_MCELLR_GDAT_DATA_DIR)
        mcellr_gdat_res = os.path.join(self.test_work_path, MCELLR_GDAT_DATA_DIR)
        
        print("PATH:" + mcellr_gdat_res)
        gdat_files = os.listdir(mcellr_gdat_res) 
        print("F1:" + str(gdat_files))
        gdat_files = [ f for f in gdat_files if f.endswith('.gdat')]
        print("F2:" + str(gdat_files))
        if gdat_files:
            # remove whole directory
            if os.path.exists(mcellr_gdat_reference):
                log("Cleaning old data in " + mcellr_gdat_reference)
                shutil.rmtree(mcellr_gdat_reference)
                
            log("Updating reference .gdat files " + mcellr_gdat_reference + " with data from " + mcellr_gdat_res)
            if not os.path.exists(mcellr_gdat_reference):
                os.makedirs(mcellr_gdat_reference)
            for f in gdat_files:
                log("Updating reference file '" + f + "'")
                shutil.copyfile(os.path.join(mcellr_gdat_res, f), os.path.join(mcellr_gdat_reference, f))

    def should_be_skipped_for_datamodel_mdl_test(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'skip_datamodel_mdl')):
            log("SKIP DATAMODEL: " + self.test_name)
            return True
        else:
            return False

    def test(self) -> int:
        if self.should_be_skipped_for_datamodel_mdl_test():
            return SKIPPED

        if self.should_be_skipped():
            return SKIPPED
            
        if self.is_known_fail():
            return KNOWN_FAIL
        
        self.clean_and_create_work_dir()
        
        res = self.run_dm_to_mdl_conversion(os.path.join(self.test_src_path, self.test_name + '.json'))
        if res != PASSED:
            return res
        
        self.change_viz_output_to_ascii()
         
        mcell_args = MCELL_BASE_ARGS.copy()
        if self.mcell4_testing:
            mcell_args.append('-mcell4')
            
        res = self.run_mcell(mcell_args, os.path.join(self.test_work_path, MAIN_MDL_FILE))
        
        if self.is_todo_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec() and not self.is_todo_test():
            return res
        
        if not UPDATE_REFERENCE:
            res = self.check_reference_data(SEED_DIR, viz_ref_required=False)
        else:
            self.update_reference()
        
        return res
