"""
Copyright (C) 2019,2020 by
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
Practically the same as tester_pymcell, however the prerequisites are different 
and the check cannot be easily parametrized. Quite probably it will evolve more 
in the future. 
"""

import os
import sys
import shutil
import subprocess
from typing import List, Dict

from test_settings import *
from tester_base import TesterBase
from tester_nutmeg import TesterNutmeg, TestDescriptionParser, STDOUT_FILE_NAME, STDERR_FILE_NAME, RunInfo
from test_utils import log_test_error, log_test_success
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


SEED_DIR = 'seed_00001'


class TesterNutmegPymcell4(TesterNutmeg):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.pymcell4_lib):
            fatal_error("Could not find library '" + tool_paths.pymcell4_lib + ".")

    def run_pymcell4_for_nutmeg(self, run_info: RunInfo) -> int:
        # we need to set the path to the build using MCELL_DIR system variable
        # and the command will be executed as shell
        cmdstr = 'export ' + MCELL_DIR_VARIABLE + '=' + self.tool_paths.mcell_dir_path + ';'
        cmdstr +=  self.tool_paths.python_binary + ' ' + os.path.join(self.test_src_path, run_info.py_file)
        cmdstr += str.join(" ", run_info.command_line_options)
        cmd = [ cmdstr ]
        
        log_name = self.test_name+'.pymcell4.log'
        fout = open(os.path.join(self.test_work_path, STDOUT_FILE_NAME), "w")
        ferr = open(os.path.join(self.test_work_path, STDERR_FILE_NAME), "w")
        flog = open(os.path.join(self.test_work_path, log_name), "w")
                
        flog.write(cmdstr + ")\ncwd: " + self.test_work_path + "\n")
        
        run_res = subprocess.run(cmd, shell=True, stdout=fout, stderr=ferr, cwd=self.test_work_path, timeout=MCELL_TIMEOUT)
        exit_code = run_res.returncode
        
        fout.close()
        ferr.close()
        
        return exit_code

    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED

        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        # transform the result ito something more readable or keep as dictionary?
        parser = TestDescriptionParser(self.test_src_path)
        test_description = parser.parse_test_description()
        if test_description is None:
            return FAILED_NUTMEG_SPEC        

        # run pymcell4
        mcell_ec = self.run_pymcell4_for_nutmeg(test_description.run_info)

        # run all checks
        for check in test_description.check_infos:
            res = self.run_check(check, mcell_ec)
            if res != PASSED:
                return res

        if res == PASSED:
            log_test_success(self.test_name, self.tester_name)
        else:
            log_test_error(self.test_name, self.tester_name, "Nutmeg testing failed")
            
        return res
