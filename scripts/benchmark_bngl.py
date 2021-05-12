"""
Copyright (C) 2020 by
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
from benchmark_mdl import BenchmarkMdl
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


class BenchmarkBngl(BenchmarkMdl):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        BenchmarkMdl.check_prerequisites(tool_paths)        
        
    def run_pymcell_w_stats(self, model_file, log_name: str) -> int:

        export_str = 'export ' + MCELL_PATH_VARIABLE + '=' + self.tool_paths.mcell_path + '; '
        perf_str = 'perf stat -e instructions:u '
        mcell_run_str =  self.tool_paths.python_binary + ' ' + os.path.join(self.test_work_path, model_file)
        
        
        if not self.tool_paths.opts.gen_benchmark_script:
            cmd = [export_str + perf_str + mcell_run_str]
            # run twice and use the second result 
            for i in range(2):
                exit_code = run(cmd, shell=True, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
                if exit_code:
                    self.log_test_error("Pymcell4 failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
                    return FAILED_MCELL
            return PASSED
        else:
            # do not run the benchmark, apped it to a script instead
            with open(self.tool_paths.benchmark_script, 'a') as f:
                f.write('echo \*\*\* ' + self.test_name + '\*\*\*\n')
                f.write('cd ' + os.getcwd() + '\n')
                
                if not self.tool_paths.opts.gen_benchmark_script_mem:
                    f.write(export_str + mcell_run_str + ' > bench.' + log_name + ' 2>&1\n')
                    f.write('grep "Simulation CPU time without iteration 0" bench.' + log_name + '\n')
                else:
                    f.write(export_str)
                    f.write('valgrind --tool=massif --pages-as-heap=yes --massif-out-file=massif.out ')
                    f.write(mcell_run_str + ' > bench.' + log_name + ' 2>&1 \n')
                    f.write('grep mem_heap_B massif.out | sed -e \'s/mem_heap_B=\(.*\)/\\1/\' | sort -g | tail -n 1\n')
                
                f.write('echo "----"\n\n')
            return SKIPPED
        
    def copy_pymcell4_benchmark_runner_and_test(self):
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'benchmark.py'),
            self.test_work_path 
        )
        
        shutil.copy(
            os.path.join(self.test_src_path, 'test.bngl'),
            self.test_work_path 
        )
        
    def copy_customization(self):
        cust_file = os.path.join(self.test_src_path, 'customization.py')
        if os.path.exists(cust_file):
            shutil.copy(
                cust_file,
                self.test_work_path 
            )
        
        
    def test(self) -> int:
        if self.should_be_skipped() and not self.tool_paths.opts.gen_benchmark_script:
            return SKIPPED
            
        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        self.copy_customization()
            
        if self.mcell4_testing:
            self.copy_pymcell4_benchmark_runner_and_test()
        
            log_name = self.test_name+'.pymcell4.log'
            res = self.run_pymcell_w_stats('benchmark.py', log_name)
        else:
            # TODO: no partitioning is generated
            res = self.convert_bngl_to_mdl()
            if res != PASSED:
                return res              
            log_name = self.test_name+'.mcell.log' 
            res = self.run_mcell_w_stats([], os.path.join('..', self.test_work_path, MAIN_MDL_FILE), log_name)

        if self.is_todo_test():
            return TODO_TEST

        if res != PASSED:
            return res
        
        res = self.benchmark_report(log_name)
        
        return res
