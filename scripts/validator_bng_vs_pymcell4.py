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
from test_utils import log_test_error
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


ONLY_BNG = False
ONLY_MCELL4_AND_BNG = False 

DEFALT_TOLERANCE_PERCENTS = 0.5 


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
        
        if res == PASSED:
            self.postrocess_mcell3r(seed)
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
    
    
    def unify_counts_with_bng_analyzer(self, counts, pymcell4):
        suffix = '4' if pymcell4 else '3'
        tmp_counts_file = 'bng_counts' + suffix + '.tmp'
        res_counts_file = 'bng_counts' + suffix + '.res'
        # prepare input
        with open(tmp_counts_file, 'w') as f:
            for k,c in counts.items():
                f.write(k + ' ' + str(c) + '\n')
                
                
        cmd = [self.tool_paths.bng_analyzer_binary, tmp_counts_file, '-o', res_counts_file]
        log_name = self.test_name+'.bng_analyzer.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if exit_code != 0:
            log_test_error(self.test_name, self.tester_name, "Bng analyzer failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return None
        
        res_counts = {}
        with open(res_counts_file, 'r') as f:
            for line in f:
                split_line = line.split()
                res_counts[split_line[0]] = float(split_line[1]) 
                
        return res_counts
        
        
    def check_res_code(self, seed, res_code):
        if res_code != PASSED:
            log_test_error(self.test_name, self.tester_name, 
                "Run with seed " + str(s) + " in work dir " + self.test_src_path + 
                " failed (only first fail is reported). "
                "See '" + os.path.join(self.test_work_path, self.test_name+'.pymcell.log') + "'.")
            return False
        else:
            return True
        
    
    def get_species_counts(self, seeds, res_codes, suffix):
        counts = {}
        for i in range(len(seeds)):
            s = seeds[i]
            if not self.check_res_code(s, res_codes[i]):
                return None
                
            last_file = self.find_last_viz_file('viz_data' + suffix + '/seed_' + str(s).zfill(5))
            if not last_file:
                log_test_error(self.test_name, self.tester_name, 
                    "Run with seed " + str(s) + " in work dir " + self.test_work_path + 
                    " - did not find output viz data file")
                return None
            curr_counts = self.get_molecule_counts_from_ascii_file(last_file)
            
            # add values with common key
            counts = Counter(counts) + Counter(curr_counts)
        return counts 


    def get_last_line(self, file):
        last_line = ''
        with open(file, 'r') as f:
            for line in f:
                if line:
                    last_line = line
        return last_line

                    
    def get_last_line_count(self, file):
        return float(self.get_last_line(file).split()[1])
    

    def get_molecule_counts(self, seeds, res_codes, suffix):
        counts = {}
        for i in range(len(seeds)):
            s = seeds[i]
            if not self.check_res_code(s, res_codes[i]):
                return None
                
            react_dir = 'react_data' + suffix + '/seed_' + str(s).zfill(5)
            if not os.path.exists(react_dir):
                log_test_error(self.test_name, self.tester_name, 
                    "Run with seed " + str(s) + " in work dir " + self.test_work_path + 
                    " - did not find react_data directory " + react_dir)
                return None
            
            file_list = os.listdir(react_dir)
            for file in file_list:
                file_path = os.path.join(react_dir, file)
                if os.path.isfile(file_path) and file.endswith('.dat'):
                    cnt = self.get_last_line_count(file_path)
                    observable = os.path.splitext(file)[0]
                    if observable.endswith('_MDLString'):
                        observable = observable[:-len('_MDLString')] 
                    if observable in counts: 
                        counts[observable] += cnt
                    else:
                        counts[observable] = cnt
                
        return counts 

    
    def get_molecule_counts_for_multiple_runs(self, pymcell4, seeds):
        
        # Set up the parallel task pool to use all available processors
        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpu_count)
        
        # Run the jobs
        if pymcell4:
            suffix = '4'
            res_codes = pool.map(self.run_validation_pymcell4, seeds)
        else:
            suffix = ''
            res_codes = pool.map(self.run_validation_mcell3r, seeds)
    
        if os.path.exists(os.path.join(self.test_src_path, 'molecule_counts')): 
            # use observables from react_output
            counts = self.get_molecule_counts(seeds, res_codes, suffix)
        else:
            # use molecule counts
            counts = self.get_species_counts(seeds, res_codes, suffix)

    
        # unify the counts, return None on error
        if counts is not None:
            if not pymcell4:
                unified_counts = self.unify_counts_with_bng_analyzer(counts, pymcell4)
            else:
                unified_counts = dict(counts)
            return unified_counts
        else:
            return None
    
    
    def generate_seeds(self, count):
        res  = []
        
        random.seed(a=200)
        for i in range(0, count):
            res.append(random.randint(1, 65535))
            
        return res    


    def gen_last_it_bng_observables_counts(self):
        first_line = ''
        
        with open('test.gdat', 'r') as f:
            first_line = f.readline()
            
        last_line = self.get_last_line('test.gdat')
                
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
    
    
    def print_counts(self, cat, counts):
        print(cat + ':')
        for k,v in sorted(counts.items()):
            print(k.ljust(30) + ' ' + format(v, '.4f'))
        print('')
        
    
    def validate_mcell_output(self, mcell3_counts, mcell4_counts, bng_counts, tolerance):
        self.print_counts("MCell3R", mcell3_counts)
        self.print_counts("MCell4", mcell4_counts)
        self.print_counts("BNG", bng_counts)
        
        print('\n--- Validation results ---')
        
        observables_missing_in_bng = []
        
        res = PASSED
        for key,cnt in sorted(mcell4_counts.items()):
            bng_name = key.replace('(', '').replace(')', '').replace('~', '').replace('!', '').replace('.', '').replace(',', '')
            mcell4_counts = cnt
            if bng_name in bng_counts:
                bng_count = bng_counts[bng_name]
                diff_perc = format(abs(((mcell4_counts / bng_count) - 1.0) * 100), '.3f')
            else:
                bng_count = -1
                diff_perc = 'NA'
                observables_missing_in_bng.append((bng_name, key))
            
            if key in mcell3_counts:
                mcell3_num = mcell3_counts[key]
            else:
                mcell3_num = -1

            less_than1_msg = ''
            if mcell4_counts < 1 and bng_count < 1:
                less_than1_msg = ' (both are < 1)'
            
            print(key.ljust(30) + ': ' + diff_perc + less_than1_msg + \
                  '% (MCell4: ' + format(mcell4_counts, '.4f') + \
                  ', BNG: ' + format(bng_count, '.4f') + 
                  ', MCell3: ' + format(mcell3_num, '.4f') + ')')
            
            if less_than1_msg == '' and bng_count != -1 and float(diff_perc) > tolerance:
                print('  - ERROR: difference against BNG is higher than tolerance of ' + str(tolerance) + '%')
                res = FAILED_VALIDATION
        
        print('--------------------------\n')
        
        if observables_missing_in_bng:
            print('ERROR: missing observables in BNG, add following lines to the bngl file:')
            for (obs_name, pat) in observables_missing_in_bng:
                print('    Species ' + obs_name + ' ' + pat)
            res = FAILED_VALIDATION
        
        if res == PASSED:
            print('PASSED')
        else:
            print('FAILED: differences are too large')
        
        return res
        
    def get_tolerance(self):
        tolerance = DEFALT_TOLERANCE_PERCENTS
        fname = os.path.join(self.test_src_path, 'tolerance')
        if os.path.exists(fname):
            with open(fname, 'r') as f:
                tolerance = float(f.readline().strip())
                print('Overriding default tolerance to ' + str(tolerance) + '%')
        return tolerance
        
    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED
        
        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        self.copy_pymcell4_runner_and_test()
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'validation_model.py'),
            self.test_work_path 
        )

        if not ONLY_BNG:
            num_runs = self.tool_paths.opts.validation_runs
            
            seeds = self.generate_seeds(num_runs)
            
            mcell3r_counts_per_run = {}
            if not ONLY_MCELL4_AND_BNG:
                # run mcell3r
                res = self.convert_bngl_to_mdl()
                if res != PASSED:
                    return res
                
                mcell3r_counts = self.get_molecule_counts_for_multiple_runs(False, seeds)
                if mcell3r_counts is None:
                    return FAILED_MCELL
                mcell3r_counts_per_run = { key:cnt/num_runs for key,cnt in mcell3r_counts.items() }
                                    
            # run pymcell4 with different seeds
            # we simply count the resulting molecules with the viz output afterwards    
            pymcell4_counts = self.get_molecule_counts_for_multiple_runs(True, seeds)
            if pymcell4_counts is None:
                return FAILED_MCELL
            pymcell4_counts_per_run = { key:cnt/num_runs for key,cnt in pymcell4_counts.items() }
        
        # run bng - we are usign ODE (at least for now), so a single run is sufficient
        bng_counts = self.run_bng_and_get_counts()
        if ONLY_BNG:
            self.print_counts("BNG", bng_counts)
        
        tolerance = self.get_tolerance()
        
        # process output
        if not ONLY_BNG:
            res = self.validate_mcell_output(mcell3r_counts_per_run, pymcell4_counts_per_run, bng_counts, tolerance)
        else:
            res = PASSED

        if self.is_todo_test():
            return TODO_TEST
       
        return res
