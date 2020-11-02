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
from typing import List, Dict

from test_settings import *
from tester_bngl_pymcell4 import TesterBnglPymcell4
from test_utils import log_test_error, find_in_file, replace_in_file
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


ONLY_BNG = False
ONLY_MCELL4_AND_BNG = False 

DEFALT_TOLERANCE_PERCENTS = 0.5 

TEST_BNGL = 'test.bngl'
TEST_GDAT = 'test.gdat'



class ValidatorBngVsPymcell4(TesterBnglPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
        needs_viz_output_each_time_step = False
    
    
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
            os.path.join(self.test_src_path, TEST_BNGL),
            self.test_work_path 
        )

    
    def merge_counts(self, dst, src):
        for k,v in src.items():
            if k in dst:
                dst[k] += v
            else:
                dst[k] = v
            
            
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
        res = self.run_pymcell4(
            test_dir=self.test_work_path, 
            test_file='validation_model.py', 
            extra_args = ['-viz-each-time-step'] if self.needs_viz_output_each_time_step else [],
            seed=seed, 
            timeout_sec=VALIDATION_TIMEOUT
            )
        
        return res
    
    
    def run_validation_mcell3r(self, seed):
        res = self.run_mcell( 
            [],
            os.path.join('..', self.test_work_path, MAIN_MDL_FILE), 
            seed=seed,
            timeout_sec=VALIDATION_TIMEOUT)
        
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
        
        
    def check_res_code(self, seed, res_code, tool):
        if res_code != PASSED:
            log_test_error(self.test_name, self.tester_name, 
                "Run of " + tool + " with seed " + str(seed) + " in work dir " + self.test_src_path + 
                " failed (only first fail is reported). ")
            return False
        else:
            return True
        
    
    def get_species_counts(self, seeds, res_codes, suffix):
        tool = 'MCell4' if suffix == '4' else 'MCell3R'
        counts = {}
        for i in range(len(seeds)):
            s = seeds[i]
            if not self.check_res_code(s, res_codes[i], tool):
                return None
                
            last_file = self.find_last_viz_file('viz_data' + suffix + '/seed_' + str(s).zfill(5))
            if not last_file:
                log_test_error(self.test_name, self.tester_name, 
                    "Run of " + tool + " with seed " + str(s) + " in work dir " + self.test_work_path + 
                    " - did not find output viz data file")
                return None
            curr_counts = self.get_molecule_counts_from_ascii_file(last_file)
            
            # add values with common key
            self.merge_counts(counts, curr_counts)

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
            if not self.check_res_code(s, res_codes[i], suffix):
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
            # use molecule counts from viz output
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
            new_seed = random.randint(1, 65535)
            while new_seed in res:
                new_seed = random.randint(1, 65535)
            res.append(new_seed)
            
        return res    


    def get_last_it_bng_observables_counts(self, dir):
        first_line = ''
        
        gdat_file = os.path.join(self.test_work_path, dir, TEST_GDAT)
                
        with open(gdat_file, 'r') as f:
            first_line = f.readline()
            
        last_line = self.get_last_line(gdat_file)
                
        observables = first_line.split()[2:]
        counts = last_line.split()[1:] # no leading '#'
                
        assert len(observables) == len(counts)
        res = {observables[i]: float(counts[i]) for i in range(len(observables))} 
        return res
        
        
    def run_validation_bng(self, dir):
        
        cmd = [ self.tool_paths.bng2pl_script, TEST_BNGL ]
        
        dir = os.path.join(self.test_work_path, dir)
        log_name = self.test_name+'.bng2pl.log'
        # run in work dir
        exit_code = run(cmd, shell=True, cwd=dir, verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        
        if (exit_code):
            log_test_error(self.test_name, self.tester_name, "BNG2.pl failed, see '" + os.path.join(dir, log_name) + "'.")
            return FAILED_BNG2PL
        else:
            return PASSED

    
    def run_bng_and_get_counts(self, seeds):
        
        # nfsim or ode?
        # does not handle comments
        line = find_in_file(TEST_BNGL, 'method=>"nf"')
        if not line:
            # ODE
            dir = 'ode'
            os.mkdir(dir)
            shutil.copy(TEST_BNGL, dir)
                     
            self.run_validation_bng(dir)
            return self.get_last_it_bng_observables_counts(dir)
        else:
            # NFSim - multiple runs are needed
            dirs = []
            for s in seeds:
                dir = 'nf_' + str(s).zfill(5)
                os.mkdir(dir)
                shutil.copy(TEST_BNGL, dir)
                # update seed value
                replace_in_file(os.path.join(dir, TEST_BNGL), 'seed=>1', 'seed=>' + str(s))
                dirs.append(dir)
            
            cpu_count = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=cpu_count)

            # run in parallel        
            res_codes = pool.map(self.run_validation_bng, dirs)
            
            # check exit codes
            for c in res_codes:
                if c != PASSED:
                    return None
            
            # colect results
            counts = {}
            for d in dirs:
                curr_counts = self.get_last_it_bng_observables_counts(d)
                self.merge_counts(counts, curr_counts)
                
            # average them directly
            res = {}
            for name,count in counts.items():
                res[name] = float(count)/len(seeds)
            return res
            
    
        
    def log_report(self, msg):
        print(msg)
        with open(os.path.join(self.test_work_path, 'validation_report.txt'), 'a+') as f:
            f.write(msg + '\n')
            
                
    def print_counts(self, cat, counts):
        self.log_report(cat + ':')
        
        if counts is None:
            self.log_report("None - error occured while obtaining data")
            return
        
        for k,v in sorted(counts.items()):
            self.log_report(k.ljust(30) + ' ' + format(v, '.4f'))
        self.log_report('')
        
    
    def validate_mcell_output(self, mcell3_counts, mcell4_counts, bng_counts, tolerance):
        self.print_counts("MCell3R", mcell3_counts)
        self.print_counts("MCell4", mcell4_counts)
        if bng_counts:
            self.print_counts("BNG", bng_counts)
        
        mcell3r_vs_mcell4 = False # default is bng vs mcell4
        ref = 'BNG'
        if not bng_counts or os.path.exists(os.path.join(self.test_src_path, 'mcell3r_vs_mcell4')): 
            mcell3r_vs_mcell4 = True
            ref = 'MCell3R'
        
        self.log_report('\n--- Validation results MCell4 vs ' + ref + ' ---')
        
        observables_missing_in_bng = []
        
        res = PASSED
        for key,cnt in sorted(mcell4_counts.items()):
            bng_name = key.replace('(', '').replace(')', '').replace('~', '').replace('!', '').replace('.', '').replace(',', '')
            mcell4_cnt = cnt
            if bng_name in bng_counts:
                bng_cnt = bng_counts[bng_name]
                if not mcell3r_vs_mcell4:
                    if bng_cnt != 0:
                        diff_perc = format(abs(((mcell4_cnt / bng_cnt) - 1.0) * 100), '.3f')
                    else:
                        if mcell4_cnt == 0:
                            diff_perc = '0.000'
                        else:
                            diff_perc = 'NA'
            else:
                bng_cnt = -1
                diff_perc = 'NA'
                observables_missing_in_bng.append((bng_name, key))
            
            if key in mcell3_counts:
                mcell3_cnt = mcell3_counts[key]
                if mcell3r_vs_mcell4:
                    if mcell3_cnt != 0:
                        diff_perc = format(abs(((mcell4_cnt / mcell3_cnt) - 1.0) * 100), '.3f')
                    else:
                        if mcell4_cnt == 0:
                            diff_perc = '0.000'
                        else:
                            diff_perc = 'NA'                
            else:
                mcell3_cnt = -1

            less_than1_msg = ''
            if mcell4_cnt < 1:
                if mcell3r_vs_mcell4:
                    if mcell3_cnt < 1:
                        less_than1_msg = ' -- (both<1)'
                        diff_perc = ''
                else:
                    if bng_cnt < 1:
                        less_than1_msg = ' -- (both<1)'
                        diff_perc = ''
            
            self.log_report(key.ljust(30) + ': ' + diff_perc + less_than1_msg + \
                  '% (MCell4: ' + format(mcell4_cnt, '.4f') + \
                  ((', BNG: ' + format(bng_cnt, '.4f')) if bng_counts else '') + 
                  ', MCell3: ' + format(mcell3_cnt, '.4f') + ')')
            
            if less_than1_msg == '' and bng_cnt != -1 and diff_perc != 'NA' and float(diff_perc) > tolerance:
                self.log_report('  - ERROR: difference against ' + ref + ' is higher than tolerance of ' + str(tolerance) + '%')
                res = FAILED_VALIDATION
        
        print('--------------------------\n')
        
        if bng_counts and observables_missing_in_bng:
            self.log_report('ERROR: missing observables in BNG, add following lines to the bngl file:')
            for (obs_name, pat) in observables_missing_in_bng:
                self.log_report('    Species ' + obs_name + ' ' + pat)
            res = FAILED_VALIDATION
        
        if res == PASSED:
            self.log_report('PASSED')
        else:
            self.log_report('FAILED: differences are too large')
        
        return res
        
    def get_tolerance(self):
        tolerance = DEFALT_TOLERANCE_PERCENTS
        fname = os.path.join(self.test_src_path, 'tolerance')
        if os.path.exists(fname):
            with open(fname, 'r') as f:
                tolerance = float(f.readline().strip())
                print('Overriding default tolerance to ' + str(tolerance) + '%')
        return tolerance
        
        
    def check_needs_viz_output_each_time_step(self):
        # special handling for MCell3R because it does not create simulation barrier
        # for BNGL observables 
        fname = os.path.join(self.test_src_path, 'needs_viz_output_each_time_step')
        return os.path.exists(fname)
    
        
    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED
        
        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        print('Report will be printed to ' + os.path.join(self.test_work_path, 'validation_report.txt'))
        
        self.copy_pymcell4_runner_and_test()
        shutil.copy(
            os.path.join(THIS_DIR, TEST_FILES_DIR, 'validation_model.py'),
            self.test_work_path 
        )
        
        self.needs_viz_output_each_time_step = self.check_needs_viz_output_each_time_step()
            
        
        num_runs = self.tool_paths.opts.validation_runs
        seeds = self.generate_seeds(num_runs)

        if not ONLY_BNG:
            
            mcell3r_counts_per_run = {}
            if not ONLY_MCELL4_AND_BNG:
                # run mcell3r
                res = self.convert_bngl_to_mdl(only_last_viz_output=not self.needs_viz_output_each_time_step)
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
        
        if not os.path.exists(os.path.join(self.test_src_path, 'no_bng')): 
            # run bng 
            bng_counts = self.run_bng_and_get_counts(seeds)
            if ONLY_BNG:
                self.print_counts("BNG", bng_counts)
        else:
            bng_counts = {}
        
        tolerance = self.get_tolerance()
        
        # process output
        if not ONLY_BNG:
            res = self.validate_mcell_output(mcell3r_counts_per_run, pymcell4_counts_per_run, bng_counts, tolerance)
        else:
            res = PASSED

        if self.is_todo_test():
            return TODO_TEST
       
        return res
