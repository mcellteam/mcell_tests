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

UPDATE_REFERENCE=False

ARG_MCELL_TESTS_DIR = '$MCELL_TESTS_DIR'
ARG_MCELL_BUILD_DIR = '$MCELL_BUILD_DIR'


class TesterExternal(TesterBase):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        pass        
        
    def test(self) -> int:
        
        self.clean_and_create_work_dir()
        
        cmd = []
        for arg in self.args:
            arg = arg.replace(ARG_MCELL_TESTS_DIR, os.path.join(THIS_DIR, '..'))
            arg = arg.replace(ARG_MCELL_BUILD_DIR, self.tool_paths.mcell_dir_path)
            cmd.append(arg)
        
        ec = run(cmd, shell=True, cwd=self.test_work_path, verbose=True)
        if ec == 0:
            return PASSED
        else:
            return FAILED_EXTERNAL
