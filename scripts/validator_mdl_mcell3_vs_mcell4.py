"""
Copyright (C) 2020 by
The Salk Institute for Biological Studies 

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
from typing import List, Dict

from test_settings import *
from tester_base import TesterBase
from validator_bng_vs_pymcell4 import ValidatorBngVsPymcell4
from test_utils import log_test_error, find_in_file, replace_in_file
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

class ValidatorMcell3VsMcell4Mdl(ValidatorBngVsPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterBase.check_prerequisites(tool_paths)   
            
           
    def run_validation_mcell4(self, seed):
        res = self.run_mcell(
            ['-seed', str(seed), '-mcell4'], 
            os.path.join(self.test_src_path, MAIN_MDL_FILE), 
            timeout_sec=VALIDATION_TIMEOUT)
        
        return res
    
    
    def run_validation_mcell3(self, seed):
        res = self.run_mcell(
            ['-seed', str(seed)], 
            os.path.join(self.test_src_path, MAIN_MDL_FILE), 
            timeout_sec=VALIDATION_TIMEOUT)

        return res    
    
    
    def get_molecule_counts_for_multiple_mdl_runs(self, mcell4, seeds):
        
        # Set up the parallel task pool to use all available processors
        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpu_count)
        
        # Run the jobs
        if mcell4:
            suffix = '4'
            res_codes = pool.map(self.run_validation_mcell4, seeds)
            # MCell4 generates viz_output dir as well, we need to distinguish it from mcell3 run
            viz_dir = os.path.join(self.test_work_path, 'viz_data')
            shutil.move(viz_dir, viz_dir + suffix)
            
            react_dir = os.path.join(self.test_work_path, 'react_data')
            if os.path.exists(react_dir):
                shutil.move(react_dir, react_dir + suffix)
        else:
            suffix = ''
            res_codes = pool.map(self.run_validation_mcell3, seeds)
    
        if os.path.exists(os.path.join(self.test_src_path, 'molecule_counts')): 
            # use observables from react_output
            counts = self.get_molecule_counts(seeds, res_codes, suffix)
        else:
            # use molecule counts
            counts = self.get_species_counts(seeds, res_codes, suffix)

    
        # unify the counts, return None on error
        if counts is not None:
            if not mcell4:
                unified_counts = self.unify_counts_with_bng_analyzer(counts, mcell4)
            else:
                unified_counts = dict(counts)
            return unified_counts
        else:
            return None
    
    
    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED
        
        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        print('Report will be printed to ' + os.path.join(self.test_work_path, 'validation_report.txt'))
        
        num_runs = self.tool_paths.opts.validation_runs
        seeds = self.generate_seeds(num_runs)

        mcell3_counts = self.get_molecule_counts_for_multiple_mdl_runs(False, seeds)
        mcell3_counts_per_run = { key:cnt/num_runs for key,cnt in mcell3_counts.items() }

        mcell4_counts = self.get_molecule_counts_for_multiple_mdl_runs(True, seeds)
        mcell4_counts_per_run = { key:cnt/num_runs for key,cnt in mcell4_counts.items() }
                                    
        tolerance = self.get_tolerance()
        
        res = self.validate_mcell_output(mcell3_counts_per_run, mcell4_counts_per_run, {}, tolerance)

        if self.is_todo_test():
            return TODO_TEST
       
        return res
