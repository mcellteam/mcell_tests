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
import re
from typing import List, Dict

from test_settings import *
from tester_base import TesterBase
from test_utils import ToolPaths, log_test_error

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False

MCELL_BASE_ARGS = ['-seed', '1']
SEED_DIR = 'seed_00001'


class BenchmarkMdl(TesterBase):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterBase.check_prerequisites(tool_paths)        
        
    def run_mcell_w_stats(self, mcell_args: List[str], main_mdl_file: str, log_name: str) -> int:

        cmd = ['perf', 'stat', '-e', 'instructions:u' ]
        cmd += [ self.tool_paths.mcell_binary ]
        cmd += mcell_args
        cmd += [ main_mdl_file ]
        cmd += self.extra_args.mcell_args
        
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            log_test_error(self.test_name, self.tester_name, "MCell failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED
        
    def get_insns_from_log(self, log_name: str):
        pat = re.compile('[ \t]*([0-9,]+)[ \t]*instructions:u')
        with open(log_name, 'r') as f:
            for line in f:
                m = pat.search(line)
                if m:
                    insn_str = m.group(1)
                    insn_str = insn_str.replace(',', '')
                    return int(insn_str)
        return -1
        
    def compare_insns_against_reference(self, insns: int):
        ref_insns = -1
        instructions_file = os.path.join(self.test_src_path, 'instructions.txt')
        if os.path.exists(instructions_file):
            with open(instructions_file, 'r') as f:
                ref_insns = int(f.readline())
            
        print(
            self.test_name + ": " + str(insns) + " vs ref. " + str(ref_insns) + 
            " (" + "{:.3f}".format(100*float(insns)/ref_insns) + "%)"
        )
        
        if self.tool_paths.opts.update_reference:
            print(self.test_name + ": updating reference in " + instructions_file)
            with open(instructions_file, 'w') as f:
                f.write(str(insns))
            
        return PASSED
        
    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED
            
        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        mcell_args = MCELL_BASE_ARGS.copy()
        if self.mcell4_testing:
            mcell_args.append('-mcell4')
        
        log_name = self.test_name+'.mcell.log'
        res = self.run_mcell_w_stats(mcell_args, os.path.join('..', self.test_src_path, MAIN_MDL_FILE), log_name)

        if self.is_todo_test():
            return TODO_TEST

        if res != PASSED:
            return res
        
        insns = self.get_insns_from_log(log_name)
        res = self.compare_insns_against_reference(insns)
        
        return res
