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
This module contains definition of a bbase class used to run tests.
"""

import abc
import os
import sys
import shutil
from typing import List, Dict

import data_output_diff

from test_settings import *
from test_utils import ToolPaths, report_test_error, report_test_success, replace_in_file

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

# TODO: maybe move check_preconditions and other things such as initialization 
# out, 
class TesterBase:
    def __init__(self, test_src_path: str, tool_paths: ToolPaths):
        # paths to the binaries
        self.tool_paths = tool_paths

        # full path to the test        
        self.test_src_path = test_src_path
        
        # name of the specific test, e.g. 0000_1_mol_type_diffuse
        self.test_name = os.path.basename(self.test_src_path)

        # full path to the test set, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/tests/mdl/
        self.test_set_path = os.path.dirname(self.test_src_path)

        # full path to the test category, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/tests/
        self.test_category_path = os.path.dirname(self.test_set_path)

        # working directory for this specific test
        self.test_work_path = os.path.abspath(
            os.path.join(self.tool_paths.work_path,
                         os.path.basename(self.test_category_path),
                         os.path.basename(self.test_set_path),
                         self.test_name
            )
        )
        
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.mcell_binary):
            fatal_error("Could not find executable '" + self.tool_paths.mcell_binary + ".")

        data_output_diff.check_or_build_fdiff()
       
    def should_be_skipped(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'skip')):
            log("SKIP : " + self.test_name)
            return True
        else:
            return False
    
    def clean_and_create_work_dir(self) -> None:
        # work dir, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/work         
        if not os.path.exists(self.tool_paths.work_path):
            os.mkdir(self.tool_paths.work_path)

        if os.path.exists(self.test_work_path):
            # log("Erasing '" + self.test_name + "' in " + os.getcwd())
            shutil.rmtree(self.test_work_path)
            
        os.makedirs(self.test_work_path)
        os.chdir(self.test_work_path)
        
        assert self.test_work_path == os.getcwd()

    def check_reference(self, seed_dir: str, ref_dir_name: str, test_dir_name: str, exact_diff: bool, msg: str) -> int:
        ref_path = os.path.join('..', self.test_src_path, ref_dir_name, seed_dir)
        if not os.path.exists(ref_path):
            return PASSED
        
        res = data_output_diff.compare_data_output_directory(
            ref_path, 
            os.path.join(test_dir_name, seed_dir),
            exact_diff)
        
        if res != PASSED:
            report_test_error(self.test_name, msg)
        return res

    def check_reference_data(self, seed_dir: str) -> int:
        
        # TODO: report error when there are no ref data
        # has_ref_data = False
        
        res = self.check_reference(
            seed_dir, REF_VIZ_DATA_DIR, VIZ_DATA_DIR, False, "Viz data diff failed.")
        if res != PASSED:
            return res

        res = self.check_reference(
            seed_dir, REF_REACT_DATA_DIR, REACT_DATA_DIR, False, "React data diff failed.")
        if res != PASSED:
            return res

        res = self.check_reference(
            '', REF_DYN_GEOM_DATA_DIR, DYN_GEOM_DATA_DIR, True, "Dynamic geometry data diff failed.")
        if res != PASSED:
            return res

        res = self.check_reference(
            '', REF_MCELLR_GDAT_DATA_DIR, MCELLR_GDAT_DATA_DIR, True, "MCellR gdat data diff failed.")
        if res != PASSED:
            return res
     
        if res == PASSED:
            report_test_success(self.test_name)
        
        return res           

    # main_mdl_file - full path needst to be provided
    def run_mcell(self, mcell_args: List[str], main_mdl_file: str) -> int:
        cmd = [ self.tool_paths.mcell_binary ]
        cmd += mcell_args
        cmd += [ main_mdl_file ]
        
        # should we enable mcellr mode?
        mdlr_rules_file = os.path.join(self.test_work_path, MAIN_MDLR_RULES_FILE)
        if os.path.exists(mdlr_rules_file):
            cmd += [ '-r', mdlr_rules_file ]
        
        log_name = self.test_name+'.mcell.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            report_test_error(self.test_name, "MCell failed, see '" + os.path.join(self.test_name, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED
         
    def run_dm_to_mdl_conversion(self, json_file_name) -> None:
        # the conversion python script is considered a separate utility, 
        # we run it through bash 
        cmd = [ 
            PYTHON_BINARY, self.tool_paths.data_model_to_mdl_script, 
            os.path.join(self.test_src_path, json_file_name), MAIN_MDL_FILE ]
        log_name = self.test_name+'.dm_to_mdl.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name)
        if exit_code != 0:
            report_test_error(self.test_name, "JSON to mdl conversion failed, see '" + os.path.join(self.test_name, log_name) + "'.")
            return FAILED_DM_TO_MDL_CONVERSION
        else:
            return PASSED

    def change_viz_output_to_ascii(self) -> int:
        fname = os.path.join(self.test_work_path, 'Scene.viz_output.mdl')
        replace_in_file(fname, 'CELLBLENDER', 'ASCII')
        return PASSED

    @abc.abstractmethod        
    def test(self) -> int:
        pass  # derived methods return integer value PASSED, FAILED_MCELL, etc.
        