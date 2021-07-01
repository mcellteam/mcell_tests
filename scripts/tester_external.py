"""
Copyright (C) 2019 by
The Salk Institute for Biological Studies and
Pittsburgh Supercomputing Center, Carnegie Mellon University

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
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
ARG_EXE_EXT = '$EXE_EXT' # usually not needed


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
            arg = arg.replace(ARG_MCELL_BUILD_DIR, self.tool_paths.mcell_path)
            arg = arg.replace(ARG_EXE_EXT, EXE_EXT)
            cmd.append(arg)
            
        env = {MCELL_PATH_VARIABLE: self.tool_paths.mcell_path}
        ec = run(cmd, shell=True, cwd=self.test_work_path, verbose=True, extra_env=env)
        if ec == 0:
            return PASSED
        else:
            return FAILED_EXTERNAL
