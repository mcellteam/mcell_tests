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

from test_settings import *
from test_utils import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


class TesterBase:
    def __init__(self, test_dir: str, tool_paths: ToolPaths):
        # paths to the binaries
        self.tool_paths = tool_paths

        # full path to the test        
        self.test_dir = test_dir
        
        # name of the specific test, e.g. 0000_1_mol_type_diffuse
        self.test_name = os.path.basename(self.test_dir)

        # full path to the test set, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/tests_mdl/
        self.test_set_dir = os.path.dirname(self.test_dir)

        # full of the test set, e.g. tests_mdl
        self.test_set_name = os.path.basename(self.test_set_dir)

        
    @abc.abstractmethod        
    def test(self):
        pass # normally is an integer PASSED, FAILED_MCELL, ... returned
    
    
    def should_be_skipped(self):
        if os.path.exists(os.path.join(self.test_dir, 'skip')):
            log("SKIP : " + test_name)
            return True
        else:
            return False
         
    
    def clean_and_create_work_dir(self): 
        # work dir, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/work         
        if not os.path.exists(self.tool_paths.work_dir):
            os.mkdir(self.tool_paths.work_dir)
        os.chdir(self.tool_paths.work_dir)
        
        # test set dir under 'work'
        if not os.path.exists(self.test_set_name):
            os.mkdir(self.test_set_name)
        os.chdir(self.test_set_name)
        
        if os.path.exists(self.test_name):
            # log("Erasing '" + self.test_name + "' in " + os.getcwd())
            shutil.rmtree(self.test_name)
            
        os.mkdir(self.test_name)
        os.chdir(self.test_name)


    def run_mcell(self, mcell_args, main_mdl_file):
        cmd = [ self.tool_paths.mcell_binary ]
        cmd += mcell_args
        cmd += [ os.path.join('..', self.test_dir, main_mdl_file) ]
        log_name = self.test_name+'.mcell.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name)
        if (exit_code):
            report_test_error(self.test_name, "MCell failed, see '" + os.path.join(self.test_name, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED
