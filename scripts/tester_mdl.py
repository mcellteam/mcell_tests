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

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run


# all paths are relative to a which should be work
VIZ_OUTPUT_DIR = os.path.join('4.', 'viz_data')
REF_VIZ_OUTPUT_DIR = 'ref_viz_data'
SEED_DIR = 'seed_00001'
MCELL_ARGS = ['-mcell4', '-seed', '1']
MAIN_MDL_FILE = 'Scene.main.mdl'


from tester_base import TesterBase


class TesterMdl(TesterBase):
    def __init___(self, test_dir: str, tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, tool_paths)
    
    
    def check_prerequisites(): 
        if not os.path.exists(MCELL_BINARY):
                fatal_error("Could not find executable '" + MCELL_BINARY + ".") 
  

    def run_mcell(test_name, test_dir):
        cmd = [ os.path.join('..', MCELL_BINARY) ]
        cmd += MCELL_ARGS
        cmd += [ os.path.join('..', test_dir, MAIN_MDL_FILE) ]
        log_name = test_name+'.mcell.log'
        exit_code = run(cmd, cwd=os.getcwd(),  fout_name=log_name)
        if (exit_code):
            report_test_error(test_name, "MCell failed, see '" + os.path.join(test_name, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED


    def check_viz_output(test_name, test_dir):
        res = viz_output_diff.compare_viz_output_directory(
            os.path.join('..', test_dir, REF_VIZ_OUTPUT_DIR, SEED_DIR), 
            os.path.join(VIZ_OUTPUT_DIR, SEED_DIR))
        
        if res == PASSED:
            report_test_success(test_name) # fail is already reported in diff
        else:
            report_test_error(test_name, "Diff failed.")
        return res
        

    def test():
        test_name = os.path.basename(test_dir)
    
        if os.path.exists(os.path.join(test_dir, 'skip')):
            log("SKIP : " + test_name)
            return SKIPPED
    
        if os.path.exists(test_name):
            print("rmtree " + test_name)
            #shutil.rmtree(test_name)
            
        os.mkdir(test_name)
        os.chdir(test_name)
        
        res = run_mcell(test_name, test_dir)
    
        if res == PASSED:
            res = check_viz_output(test_name, test_dir)
    
        os.chdir('..')
        return res
