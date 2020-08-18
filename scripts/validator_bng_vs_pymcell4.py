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


RUN_MCELL3R = True

NUM_MCELL_VALIDATION_RUNS = 24

TOLERANCE_PERC = 0.5 


class ValidatorBngVsPymcell4(TesterBnglPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.pymcell4_lib):
            fatal_error("Could not find library '" + tool_paths.pymcell4_lib + ".")
        if not tool_paths.bng2pl_script:
            fatal_error("Path to bionetgen must be set using -n.")
        if not os.path.exists(tool_paths.bng2pl_script):
            fatal_error("Could not find script '" + tool_paths.bng2pl_script + ".")
            
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
    
           
    def run_validation_pymcell4(self, seed):
        res = self.run_pymcell(test_dir=self.test_work_path, test_file='validation_model.py', extra_args=['-seed', str(seed)])
        return res
    
    def run_validation_mcell3r(self, seed):
        res = self.run_mcell(['-seed', str(seed)], os.path.join('..', self.test_work_path, MAIN_MDL_FILE))
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
    
    
    def get_molecule_counts_for_multiple_runs(self, pymcell4, seeds):
        counts = {}
        current_run = 1
        
        # Set up the parallel task pool to use all available processors
        count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=count)
        
        # Run the jobs
        if pymcell4:
            res_codes = pool.map(self.run_validation_pymcell4, seeds)
        else:
            res_codes = pool.map(self.run_validation_mcell3r, seeds)
    
        #for s in seeds:
        for i in range(len(seeds)):
            s = seeds[i]
            if res_codes[i] != PASSED:
                log_test_error(self.test_name, self.tester_name, 
                    "Run with seed " + str(s) + " in work dir " + self.test_src_path + 
                    " failed (only first fail is reported). "
                    "See '" + os.path.join(self.test_work_path, self.test_name+'.pymcell.log') + "'.")
                return None
                
            last_file = self.find_last_viz_file('viz_data/seed_' + str(s).zfill(5))
            if not last_file:
                log_test_error(self.test_name, self.tester_name, 
                    "Run with seed " + str(s) + " in work dir " + self.test_src_path + 
                    " - did not find output viz data file")
                return None
            curr_counts = self.get_molecule_counts_from_ascii_file(last_file)
            
            # add values with common key
            counts = Counter(counts) + Counter(curr_counts) 
    
        return dict(counts)
    
    
    def generate_seeds(self, count):
        res  = []
        
        random.seed(a=200)
        for i in range(0, count):
            res.append(random.randint(1, 65535))
            
        return res    


    def gen_last_it_bng_observables_counts(self):
        first_line = ''
        last_line = ''
        with open('test.gdat', 'r') as f:
            first_line = f.readline()
            for line in f:
                if line:
                    last_line = line
                
        observables = first_line.split()[2:]
        counts = last_line.split()[1:] # no leading '#'
                
        assert len(observables) == len(counts)
        res = {observables[i]: float(counts[i]) for i in range(len(observables))} 
        return res
        

    def run_bng_and_get_counts(self):
        # we need to set the path to the build using MCELL_DIR system variable
        # and the command will be executed as shell
        cmd = [ self.tool_paths.bng2pl_script, 'test.bngl' ]
        
        log_name = self.test_name+'.bng2pl.log'
        # run in work dir
        exit_code = run(cmd, shell=True, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            log_test_error(self.test_name, self.tester_name, "BNG2.pl failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return None
        
        return self.gen_last_it_bng_observables_counts()
    
    
    def validate_mcell_output(self, mcell_counts, bng_counts):
        print("MCell4:" + str(mcell_counts))
        print("BNG:" + str(bng_counts))
        
        print('Validation results:')
        
        res = PASSED
        for key,cnt in mcell_counts.items():
            bng_name = key.replace('(', '').replace(')', '').replace('~', '').replace('!', '').replace('.', '')
            mcell_counts = cnt
            bng_count = bng_counts[bng_name]
            diff_perc = abs(((mcell_counts / bng_count) - 1.0) * 100)
            print(key + ': ' + format(diff_perc, '.3f') + '% (MCell: ' + str(mcell_counts) + ', BNG: ' + str(bng_count) + ')')
            if diff_perc > TOLERANCE_PERC:
                print('  - ERROR: difference is higher than tolerance of ' + str(TOLERANCE_PERC) + '%')
                res = FAILED_VALIDATION
        
        if res == PASSED:
            print('PASSED')
        else:
            print('FAILED: differences are too large')
        
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

        seeds = self.generate_seeds(NUM_MCELL_VALIDATION_RUNS)
        
        # run mcell3r
        res = self.convert_bngl_to_mdl()
        if res != PASSED:
            return res
        
        mcell3r_counts = self.get_molecule_counts_for_multiple_runs(False, seeds)
        if mcell3r_counts is None:
            return FAILED_MCELL
        mcell3r_counts_per_run = { key:cnt/NUM_MCELL_VALIDATION_RUNS for key,cnt in mcell3r_counts.items() }
        print("MCell3R:" + str(mcell3r_counts_per_run))
                                
        # run pymcell4 with different seeds
        # we simply count the resulting molecules with the viz output afterwards    
        pymcell4_counts = self.get_molecule_counts_for_multiple_runs(True, seeds)
        if pymcell4_counts is None:
            return FAILED_MCELL
        pymcell4_counts_per_run = { key:cnt/NUM_MCELL_VALIDATION_RUNS for key,cnt in pymcell4_counts.items() }
        
        # run bng - we are usign ODE (at least for now), so a single run is sufficient
        bng_counts = self.run_bng_and_get_counts()
        
        # process output
        res = self.validate_mcell_output(pymcell4_counts_per_run, bng_counts)

        if self.is_todo_test():
            return TODO_TEST
       
        return res
