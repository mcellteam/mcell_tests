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
import glob
import random
import multiprocessing
import re
from collections import Counter
from typing import List, Dict

from test_settings import *
from tester_bngl_pymcell4 import TesterBnglPymcell4
from test_utils import ToolPaths, log_test_error

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


NUM_MCELL_VALIDATION_RUNS = 16


class ValidatorBngVsPymcell4(TesterBnglPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.pymcell4_lib):
            fatal_error("Could not find library '" + tool_paths.pymcell4_lib + ".")
        # bionetgen path

    def copy_pymcell4_runner_and_test(self):
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'validation_model.py'),
            self.test_work_path 
        )
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'model.py'),
            self.test_work_path 
        )        

        shutil.copy(
            os.path.join(self.test_src_path, 'test.bngl'),
            self.test_work_path 
        )
        
    def get_molecule_counts_from_ascii_file(self, filename):
        counts = {}
        with open(filename, 'r') as fin:
            for line in fin:
                # the first item is the ID
                id = line.split(' ')[0]
                if id in counts:
                    counts[id] = counts[id] + 1
                else:
                    counts[id] = 1
                    
        return counts
    
           
    def run_validation_pymcell(self, seed):
        res = self.run_pymcell(test_dir=self.test_work_path, test_file='validation_model.py', extra_args=['-seed', str(seed)])
        return res
    
    
    def find_last_viz_file(self, dir):
        files = os.listdir(dir)
        max_it_file = ''
        max_it = -1
        for fname in files:
            if re.match('Scene\.ascii\.[0-9]+\.dat', fname):
                it = int(fname.split('.')[2])
                if it > max_it:
                    max_it = it
                    max_it_file = fname
        
        return os.path.join(dir, max_it_file)
    
    
    def get_molecule_counts_for_multiple_runs(self, seeds):
        counts = {}
        current_run = 1
        
        # Set up the parallel task pool to use all available processors
        count = 12 # multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=count)
        
        # Run the jobs
        res_codes = pool.map(self.run_validation_pymcell, seeds)
    
        #for s in seeds:
        for i in range(len(seeds)):
            s = seeds[i]
            if res_codes[i] != PASSED:
                log_test_error(self.test_name, self.tester_name, 
                    "Run of pymcell4 with seed " + str(s) + " in work dir " + self.test_src_path + 
                    " failed (only first fail is reported). "
                    "See '" + os.path.join(self.test_work_path, self.test_name+'.pymcell.log') + "'.")
                return None
                
            last_file = self.find_last_viz_file('viz_data/seed_' + str(s).zfill(5))
            curr_counts = self.get_molecule_counts_from_ascii_file(last_file)
            
            # add values with common key
            counts = Counter(counts) + Counter(curr_counts) 
    
        return counts
    
    
    def generate_seeds(self, count):
        res  = []
        
        random.seed(a=200)
        for i in range(0, count):
            res.append(random.randint(1, 65535))
            
        return res    

        
    def test(self) -> int:
        # not skipping validation tests

        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        self.copy_pymcell4_runner_and_test()
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'validation_model.py'),
            self.test_work_path 
        )
                
        # run pymcell4 with different seeds
        # we simply count the resulting molecules with the viz output afterwards    
        seeds = self.generate_seeds(NUM_MCELL_VALIDATION_RUNS)
        counts = self.get_molecule_counts_for_multiple_runs(seeds)
        if counts is None:
            return FAILED_MCELL
            
        print("MCell4:" + str(counts))
        

        # run bng
        
        # process output
            
        if self.is_todo_test():
            return TODO_TEST
        
       
        return PASSED
