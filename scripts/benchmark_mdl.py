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
import re
from typing import List, Dict

from test_settings import *
from tester_base import TesterBase
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False

MCELL_BASE_ARGS = ['-seed', '1']

class BenchmarkMdl(TesterBase):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterBase.check_prerequisites(tool_paths)        
        
    def run_mcell_w_stats(self, mcell_args: List[str], main_mdl_file: str, log_name: str) -> int:

        perf_cmd = ['perf', 'stat', '-e', 'instructions:u' ]
        mcell_run_cmd = [ self.tool_paths.mcell_binary ]
        mcell_run_cmd += mcell_args
        mcell_run_cmd += [ main_mdl_file ]
        mcell_run_cmd += self.extra_args.mcell_args
        
        mdlr_rules_file = os.path.join(self.test_work_path, MAIN_MDLR_RULES_FILE)
        if os.path.exists(mdlr_rules_file):
            mcell_run_cmd += [ '-r', mdlr_rules_file ]
        
        if not self.tool_paths.opts.gen_benchmark_script:
            for i in range(2):
                cmd = perf_cmd + mcell_run_cmd
                exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
                if (exit_code):
                    self.log_test_error("MCell failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
                    return FAILED_MCELL
            return PASSED
        else:
            mcell_run_str = ' '.join(mcell_run_cmd)
            with open(self.tool_paths.benchmark_script, 'a') as f:
                f.write('echo \*\*\* ' + self.test_name + '\*\*\*\n')
                f.write('cd ' + os.getcwd() + '\n')  
                if not self.tool_paths.opts.gen_benchmark_script_mem:
                    f.write(mcell_run_str + ' > bench.' + log_name + ' 2>&1\n')
                    f.write('grep "Simulation CPU time without iteration 0" bench.' + log_name + '\n')
                else:
                    f.write('valgrind --tool=massif --pages-as-heap=yes --massif-out-file=massif.out ')
                    f.write(mcell_run_str + ' > bench.' + log_name + ' 2>&1\n')
                    f.write('grep mem_heap_B massif.out | sed -e \'s/mem_heap_B=\(.*\)/\\1/\' | sort -g | tail -n 1\n')
                    
                f.write('echo "----"\n\n')
            return SKIPPED
        
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
        
    def benchmark_report(self, log_name: str):
        insns = self.get_insns_from_log(log_name)
        ref_insns = -1
        instructions_file = os.path.join(self.test_src_path, 'instructions.txt')
        if os.path.exists(instructions_file):
            with open(instructions_file, 'r') as f:
                ref_insns = int(f.readline())
            
        print(
            self.test_name + ": " + str(insns) + " vs ref. " + str(ref_insns) + 
            " (" + "{:.3f}".format(100*float(insns)/ref_insns) + "%)"
        )
        
        if self.tool_paths.opts.extra_reports:
            with open(log_name, 'r') as f:
                for line in f:
                    if 'Simulation CPU time' in line:
                        print(line)
        
        if self.tool_paths.opts.update_reference:
            print(self.test_name + ": updating reference in " + instructions_file)
            with open(instructions_file, 'w') as f:
                f.write(str(insns))
            
        return PASSED
    
    
        
    def test(self) -> int:
        if self.should_be_skipped() and not self.tool_paths.opts.gen_benchmark_script:
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
        
        res = self.benchmark_report(log_name)
                    
        return res
