#!/usr/bin/env python3

"""
Copyright (C) 2019,2020 by
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

"""
This module contains diverse utility functions shared among all mcell-related 
Python scripts.

TODO: some sanity checks would be useful - e.g. testing that it can detect 
that reference and new data are indeed different.

TODO: build fdiff automatically
"""

import os
import sys
import subprocess
import multiprocessing
import itertools 
import re
import argparse
import shutil
import time
import psutil
from threading import Timer
from typing import List, Dict
import toml


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, 'scripts'))

from test_settings import *
from tool_paths import ToolPaths

# import tester classes
from tester_mdl import TesterMdl
from tester_base import get_tester_name
from tester_data_model import TesterDataModel
from tester_data_model_converter import TesterDataModelConverter
from tester_nutmeg import TesterNutmeg
from tester_pymcell import TesterPymcell
from tester_python import TesterPython
from tester_pymcell4 import TesterPymcell4
from tester_data_model_pymcell4 import TesterDataModelPymcell4
from tester_mdl_data_model_pymcell4 import TesterMdlDataModelPymcell4
from tester_nutmeg_pymcell4 import TesterNutmegPymcell4
from tester_bngl_mcell3r import TesterBnglMcell3R
from tester_bngl_pymcell4 import TesterBnglPymcell4
from tester_bngl_pymcell4_export import TesterBnglPymcell4Export
from tester_bngl_data_model_pymcell4 import TesterBnglDataModelPymcell4
from tester_external import TesterExternal
from benchmark_mdl import BenchmarkMdl
from benchmark_bngl import BenchmarkBngl
from benchmark_mdl_data_model_pymcell4 import BenchmarkMdlDataModelPymcell4
from validator_bng_vs_pymcell4 import ValidatorBngVsPymcell4
from validator_mdl_mcell3_vs_mcell4 import ValidatorMcell3VsMcell4Mdl

sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))

from utils import run, log, fatal_error

DEFAULT_CONFIG_PATH = os.path.join('test_configs', 'default.toml')
KEY_SET = 'set'
KEY_INCLUDE = 'include'
KEY_FILE = 'file'
KEY_CATEGORY = 'category'
# TODO: these keys should use lowercase with underscores naming
KEY_TEST_SET = 'testSet'
KEY_TESTER_CLASS = 'testerClass'
KEY_TEST_DIR_SUFFIX = 'testDirSuffix'
KEY_ARGS = 'args'


class TestOptions:
    def __init__(self):
        self.sequential = False
        self.config = DEFAULT_CONFIG_PATH
        self.pattern = None
        self.max_cores = None
        self.mcell_build_path_override = None
        self.cellblender_build_path_override = None
        self.bionetgen_path = None
        self.python_binary_override = None    
        self.update_reference = False
        self.validation_runs = DEFAULT_VALIDATION_RUNS

    def __repr__(self):
        attrs = vars(self)
        return ", ".join("%s: %s" % item for item in attrs.items())
            
# FIXME: insert into TestOptions class         
def create_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='MCell testing tool')
    parser.add_argument('-s', '--sequential', action='store_true', help='run testing sequentially (default is parallel)')
    parser.add_argument('-c', '--config', type=str, help='load testing config from a specified file (default is test_configs/default.toml')
    parser.add_argument('-p', '--pattern', type=str, help='regex pattern to filter tests to be run, the pattern is matched against the test path')
    parser.add_argument('-j', '--max-cores', type=str, help='sets maximum number of cores for testing, default all if -s is not used')
    parser.add_argument('-m', '--mcell-build-path', type=str, help='override of the default mcell build path')
    parser.add_argument('-b', '--cellblender-build-path', type=str, help='override of the default cellblender build path')
    parser.add_argument('-n', '--bionetgen-path', type=str, help='path leading to BNG2.pl')
    parser.add_argument('-t', '--testing-python-executable', type=str, help='override of the default python used for testing (e.g. to run conversion scripts)')
    parser.add_argument('-u', '--update-reference', action='store_true', help='update reference (works currently only for benchmarks)')
    parser.add_argument('-v', '--validation-runs', type=str, help='number of validation runs, default is ' + str(DEFAULT_VALIDATION_RUNS))
    return parser

# FIXME: insert into TestOptions class       
def process_opts() -> TestOptions:
    parser = create_argparse()
    args = parser.parse_args()
    print(args)
    
    opts = TestOptions()
    
    if args.sequential:
        opts.sequential = True
    if args.config:
        opts.config = args.config
    if args.pattern:
        opts.pattern = args.pattern

    if args.max_cores:
        opts.max_cores = int(args.max_cores)
        
    if args.mcell_build_path:
        opts.mcell_build_path_override = args.mcell_build_path 

    if args.cellblender_build_path:
        opts.cellblender_build_path_override = args.cellblender_build_path 

    if args.bionetgen_path:
        opts.bionetgen_path = args.bionetgen_path 

    if args.testing_python_executable:
        opts.python_binary_override = args.testing_python_executable 

    if args.update_reference:
        opts.update_reference = True
        
    if args.validation_runs:
        opts.validation_runs = int(args.validation_runs)
        
    return opts


class TestSetInfo:
    def __init__(self, category: str, test_set_name: str, tester_class: str, test_dir_suffix, args: List[str]):
        self.category = category  # e.g. tests or examples
        self.test_set_name = test_set_name  # e.g. nutmeg_positive
        self.tester_class = tester_class  # class derived from TesterBase
        self.test_dir_suffix = test_dir_suffix  
        self.args = args # enabled when mcell4 should be tested
        
    def has_same_base_dir(self, other):
        return \
            self.category == other.category and \
            self.test_set_name == other.test_set_name and \
            self.tester_class == other.tester_class and \
            self.test_dir_suffix == other.test_dir_suffix  
        
    def __repr__(self):
        attrs = vars(self)
        return ", ".join("%s: %s" % item for item in attrs.items())        
        
# we are only adding the specific test directory
class TestInfo(TestSetInfo):
    def __init__(self, test_set_info: TestSetInfo, test_path: str):
        self.test_path = test_path  # full path to the test directory
        super(TestInfo, self).__init__(
            test_set_info.category, test_set_info.test_set_name, test_set_info.tester_class, 
            test_set_info.test_dir_suffix, test_set_info.args)

    def __repr__(self):
        return os.path.join(self.test_path) + ' [' + get_tester_name(self.tester_class) + ']'
        #return '[' + str(self.tester_class) + ']:' + os.path.join(self.test_path)

    def get_full_name(self):
        # not using os.path.join because the name must be identical on every system
        return self.category + '/' + self.test_set_name + '/' + os.path.basename(self.test_path)
    
    def get_name_w_tester_class(self):
        return get_tester_name(self.tester_class) + self.test_dir_suffix + '/' + self.get_full_name()

    def get_full_name_for_sorting(self):
        # for sorting, we would like the long tests to be run as the first ones (due to parallel execution)
        base_name = self.category + '/' + self.test_set_name + '/' + os.path.basename(self.test_path)
        if base_name.endswith('long'):
            base_name = '0000_' + base_name 
        return base_name


# returns a list of TestInfo objects
def get_test_dirs(test_set_info: TestSetInfo) -> List[TestInfo]:
    res = []
    test_set_full_path = os.path.join(THIS_DIR, test_set_info.category, test_set_info.test_set_name)
    print("Looking for tests in " + test_set_full_path)
    files = os.listdir(test_set_full_path)
    for name in files:
        name_w_dir = os.path.join(test_set_full_path, name)
        if os.path.isdir(name_w_dir):
            res.append(TestInfo(test_set_info, name_w_dir))
    return res
   
    
def run_single_test(test_info: TestInfo, tool_paths: ToolPaths) -> int:
    start = time.time()

    test_obj = test_info.tester_class(test_info.test_path, test_info.test_dir_suffix, test_info.args, tool_paths)
    
    # do not run certain tests if one has less than ~8BG of RAM
    if os.path.exists(os.path.join(test_obj.test_src_path, 'skip_mem')) and psutil.virtual_memory().total < 8000000000:
        print("Test " + test_obj.test_src_path + " skipped due to its memory requirements.")
        return SKIPPED
    
    res = test_obj.test()
    
    end = time.time()
    #log("FINISHED: " + test_info.get_full_name() + " in " + str(round(end - start, 2)) + " s")
    return res
    
    
def get_dict_value(d: Dict, key: str, fname: str) -> str:
    if key not in d:
        fatal_error("Required field '" + key + "' not found in '" + fname + "'.")
    res = d[key]
    return res


def load_test_config(config_path: str) -> List[TestSetInfo]:
    top_dict = toml.load(config_path)
    
    config_dir = os.path.dirname(config_path)
    
    res = []
    if KEY_SET in top_dict:
        sets_list = get_dict_value(top_dict, KEY_SET, config_path)
        for set in sets_list:
            category = get_dict_value(set, KEY_CATEGORY, config_path)
            test_set_name = get_dict_value(set, KEY_TEST_SET, config_path)
            class_name = get_dict_value(set, KEY_TESTER_CLASS, config_path)
            if class_name == 'TesterMdl':
                tester_class = TesterMdl  
            elif class_name == 'TesterDataModel':
                tester_class = TesterDataModel  
            elif class_name == 'TesterDataModelConverter':
                tester_class = TesterDataModelConverter  
            elif class_name == 'TesterNutmeg':
                tester_class = TesterNutmeg
            elif class_name == 'TesterPymcell':
                tester_class = TesterPymcell
            elif class_name == 'TesterPython':                
                tester_class = TesterPython                
            elif class_name == 'TesterPymcell4':
                tester_class = TesterPymcell4
            elif class_name == 'TesterDataModelPymcell4':
                tester_class = TesterDataModelPymcell4
            elif class_name == 'TesterMdlDataModelPymcell4':
                tester_class = TesterMdlDataModelPymcell4
            elif class_name == 'TesterNutmegPymcell4':
                tester_class = TesterNutmegPymcell4
            elif class_name == 'TesterBnglMcell3R':
                tester_class = TesterBnglMcell3R
            elif class_name == 'TesterBnglPymcell4':
                tester_class = TesterBnglPymcell4
            elif class_name == 'TesterBnglPymcell4Export':
                tester_class = TesterBnglPymcell4Export
            elif class_name == 'TesterBnglDataModelPymcell4':
                tester_class = TesterBnglDataModelPymcell4
            elif class_name == 'TesterExternal':
                tester_class = TesterExternal
            elif class_name == 'BenchmarkMdl':
                tester_class = BenchmarkMdl
            elif class_name == 'BenchmarkBngl':
                tester_class = BenchmarkBngl
            elif class_name == 'BenchmarkMdlDataModelPymcell4':
                tester_class = BenchmarkMdlDataModelPymcell4
            elif class_name == 'ValidatorBngVsPymcell4':
                tester_class = ValidatorBngVsPymcell4
            elif class_name == 'ValidatorMcell3VsMcell4Mdl':
                tester_class = ValidatorMcell3VsMcell4Mdl
            else:
                fatal_error("Unknown tester class '" + class_name + "' in '" + config_path + "'.")
            
            test_dir_suffix = ''
            if KEY_TEST_DIR_SUFFIX in set:
                test_dir_suffix = get_dict_value(set, KEY_TEST_DIR_SUFFIX, config_path)
                
            args = []
            if KEY_ARGS in set:
                args = set[KEY_ARGS]
            res.append(TestSetInfo(category, test_set_name, tester_class, test_dir_suffix, args))


    if KEY_INCLUDE in top_dict:
        includes_list = get_dict_value(top_dict, KEY_INCLUDE, config_path)
        
        for include in includes_list:
            file = get_dict_value(include, KEY_FILE, config_path)
            # load included file recursively
            included_fname = os.path.join(config_dir, file)
            included_test_set_infos = load_test_config(included_fname)
            
            if KEY_TEST_DIR_SUFFIX in include:
                # append test dir suffix
                for info in included_test_set_infos:
                    info.test_dir_suffix += get_dict_value(include, KEY_TEST_DIR_SUFFIX, included_fname)
        
            res += included_test_set_infos
                          
    return res


def check_different_dirs(test_set_infos):
    num_test_sets = len(test_set_infos)
    for i in range(num_test_sets):
        curr = test_set_infos[i]
        for k in range(i + 1, num_test_sets):
            checked = test_set_infos[k]
            if curr.has_same_base_dir(checked): 
                print("Error: 2 test set infos are set to use the same directory:")
                print(str(curr))
                print(str(checked))
                sys.exit(1)
        
        
    
def collect_and_run_tests(tool_paths: ToolPaths, opts: TestOptions) -> Dict:
    
    test_set_infos = load_test_config(opts.config)
    
    check_different_dirs(test_set_infos)
    
    test_infos = []
    tester_classes = set()
    for test_set in test_set_infos:
        if test_set.tester_class != TesterExternal: 
            test_infos += get_test_dirs(test_set)
            tester_classes.add(test_set.tester_class)
        else:
            test_infos.append(TestInfo(test_set, test_set.test_set_name))
            
    filtered_test_infos = []
    for info in test_infos:
        if not opts.pattern or re.search(opts.pattern, info.test_path):
            filtered_test_infos.append(info)

    filtered_test_infos.sort(key=lambda x: x.get_full_name_for_sorting())

    log("Tests to be run:")
    for info in filtered_test_infos:
        log(str(info))

    log("Handling tester class prerequisites")
    for tester_class in tester_classes:
        tester_class.check_prerequisites(tool_paths)

    results = {}
    work_dir = os.getcwd()
    if opts.sequential:
        for info in filtered_test_infos:
            log("Testing " + info.test_path)
            res = run_single_test(info, tool_paths)
            results[info.get_name_w_tester_class()] = res
    else:
        # Set up the parallel task pool to use all available processors
        if opts.max_cores:
            count = opts.max_cores
        else:
            count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=count, maxtasksperchild=1)
 
        # Run the jobs, the last argument represents chunk size - using 1 for best load balancing  
        result_values = pool.starmap(run_single_test, zip(filtered_test_infos, itertools.repeat(tool_paths)), 1)
        
        test_names = [info.get_name_w_tester_class() for info in filtered_test_infos]
        results = dict(zip(test_names, result_values))

    os.chdir(work_dir)  # just to be sure, let's fix cwd

    return results


def report_results(results: Dict) -> int:
    print("\n**** RESULTS ****")
    passed_count = 0
    skipped_count = 0
    known_fails_count = 0
    todo_tests_count = 0
    failed_tests = []
    for key, value in results.items():
        if not value:
            fatal_error('Invalid result for ' + key)
        print(RESULT_NAMES[value] + ": " + str(key))
        if value == PASSED:
            passed_count += 1
        elif value in FAIL_CODES:
            failed_tests.append((value, key))
        elif value == SKIPPED:
            skipped_count += 1
        elif value == KNOWN_FAIL:
            known_fails_count += 1
        elif value == TODO_TEST:
            todo_tests_count += 1
        else:
            fatal_error("Invalid test result value " + str(value))

    res = 0       
    if failed_tests:
        log("\n\nFAILED TESTS:")
        for test in sorted(failed_tests):
            print(RESULT_NAMES[test[0]] + ": " + str(test[1]))
        
        log("\n!! THERE WERE ERRORS !!")
        res = 1
    else:
        log("\n-- SUCCESS --")
        res = 0

    log("PASSED: " + str(passed_count) + ", FAILED: " + str(len(failed_tests)) + ", SKIPPED: " + str(skipped_count) + 
        ", KNOWN FAILS: " + str(known_fails_count) + ", TODO TESTS: " + str(todo_tests_count))
        
    return res


def check_file_exists(name):
    if not os.path.exists(name):
        fatal_error("Required file '" + name + "' does not exist")

def run_tests() -> int:
    opts = process_opts()

    # FIXME: use arguments directly to initialize ToolPaths    
    tool_paths = ToolPaths(opts)
    log(str(tool_paths))
    
    results = collect_and_run_tests(tool_paths, opts)
    ec = report_results(results)
    return ec


if __name__ == '__main__':
    ec = run_tests()
    sys.exit(ec)
    

