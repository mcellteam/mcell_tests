#!/usr/bin/env python3

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
from datetime import datetime
from threading import Timer
from typing import List, Dict
import toml


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, 'scripts'))

from test_settings import *
from test_utils import ToolPaths

# import tester classes
from tester_mdl import TesterMdl
from tester_datamodel import TesterDataModel
from tester_nutmeg import TesterNutmeg
from tester_pymcell import TesterPymcell

sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))

from utils import run, log, fatal_error

DEFAULT_CONFIG_PATH = os.path.join('test_configs', 'default.toml')
KEY_SET = 'set'
KEY_CATEGORY = 'category'
KEY_TEST_SET = 'testSet'
KEY_TESTER_CLASS = 'testerClass'
KEY_ARGS = 'args'


class TestOptions:
    def __init__(self):
        self.sequential = False
        self.config = DEFAULT_CONFIG_PATH
        self.pattern = None
        self.mcell_build_path_override = None
        self.cellblender_build_path_override = None  

    def __repr__(self):
        attrs = vars(self)
        return ", ".join("%s: %s" % item for item in attrs.items())
            
# FIXME: insert into TestOptions class         
def create_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='MCell testing tool')
    parser.add_argument('-s', '--sequential', action='store_true', help='run testing sequentially (default is parallel)')
    parser.add_argument('-c', '--config', type=str, help='load testing config from a specified file (default is test_configs/default.toml')
    parser.add_argument('-p', '--pattern', type=str, help='regex pattern to filter tests to be run, the pattern is matched against the test path')
    parser.add_argument('-m', '--mcell-build-path', type=str, help='override of the default mcell build path')
    parser.add_argument('-b', '--cellblender-build-path', type=str, help='override of the default cellblender build path')
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
        
    if args.mcell_build_path:
        opts.mcell_build_path_override = args.mcell_build_path 

    if args.cellblender_build_path:
        opts.cellblender_build_path_override = args.cellblender_build_path 

    return opts


class TestSetInfo:
    def __init__(self, category: str, test_set_name: str, tester_class: str, args: List[str]):
        self.category = category  # e.g. tests or examples
        self.test_set_name = test_set_name  # e.g. nutmeg_positive
        self.tester_class = tester_class  # class derived from TesterBase
        self.args = args # enabled when mcell4 should be tested


# we are only adding the specific test directory
class TestInfo(TestSetInfo):
    def __init__(self, test_set_info: TestSetInfo, test_path: str):
        self.test_path = test_path  # full path to the test directory
        super(TestInfo, self).__init__(test_set_info.category, test_set_info.test_set_name, test_set_info.tester_class, test_set_info.args)

    def __repr__(self):
        return '[' + str(self.tester_class) + ']:' + os.path.join(self.test_path)

    def get_full_name(self):
        # not using os.path.join because the name must be identical on every system
        return self.category + '/' + self.test_set_name + '/' + os.path.basename(self.test_path)


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
    log("STARTED: " + test_info.get_full_name() + " at " + datetime.now().strftime('%H:%M:%S'))
    test_obj = test_info.tester_class(test_info.test_path, test_info.args, tool_paths)
    res = test_obj.test()
    log("FINISHED: " + test_info.get_full_name() + " at " + datetime.now().strftime('%H:%M:%S'))
    return res
    
    
def get_dict_value(d: Dict, key: str, fname: str) -> str:
    if key not in d:
        fatal_error("Required field '" + key + "' not found in '" + fname + "'.")
    res = d[key]
    return res
    
    
def load_test_config(config_path: str) -> List[TestSetInfo]:
    top_dict = toml.load(config_path)
    
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
            elif class_name == 'TesterNutmeg':
                tester_class = TesterNutmeg
            elif class_name == 'TesterPymcell':
                tester_class = TesterPymcell
            else:
                fatal_error("Unknown tester class '" + class_name + "' in '" + config_path + "'.")
                
            args = []
            if KEY_ARGS in set:
                args = set[KEY_ARGS]
            res.append(TestSetInfo(category, test_set_name, tester_class, args))
                  
    return res

    
def collect_and_run_tests(tool_paths: ToolPaths, opts: TestOptions) -> Dict:
    
    test_set_infos = load_test_config(opts.config)
    
    test_infos = []
    tester_classes = set()
    for test_set in test_set_infos:
        test_infos += get_test_dirs(test_set)
        tester_classes.add(test_set.tester_class)

    filtered_test_infos = []
    for info in test_infos:
        if not opts.pattern or re.search(opts.pattern, info.test_path):
            filtered_test_infos.append(info)

    filtered_test_infos.sort(key=lambda x: x.get_full_name())

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
            results[info.get_full_name()] = res
    else:
        # Set up the parallel task pool to use all available processors
        count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=count)
 
        # Run the jobs
        result_values = pool.starmap(run_single_test, zip(filtered_test_infos, itertools.repeat(tool_paths)))
        
        test_names = [info.get_full_name() for info in filtered_test_infos]
        results = dict(zip(test_names, result_values))

    os.chdir(work_dir)  # just to be sure, let's fix cwd

    return results


def report_results(results: Dict) -> int:
    print("\n**** RESULTS ****")
    passed_count = 0
    skipped_count = 0
    failed_tests = []
    for key, value in results.items():
        print(RESULT_NAMES[value] + ": " + str(key))
        if value == PASSED:
            passed_count += 1
        elif value in [FAILED_MCELL, FAILED_DIFF, FAILED_DM_TO_MDL_CONVERSION, FAILED_NUTMEG_SPEC]:
            failed_tests.append((value, key))
        elif value == SKIPPED:
            skipped_count += 1
        else:
            fatal_error("Invalid test result value " + str(value))

    res = 0       
    if failed_tests:
        log("\n\nFAILED TESTS:")
        for test in failed_tests:
            print(RESULT_NAMES[test[0]] + ": " + str(test[1]))
        
        log("\n!! THERE WERE ERRORS !!")
        res = 1
    else:
        log("\n-- SUCCESS --")
        res = 0

    log("PASSED: " + str(passed_count) + ", FAILED: " + str(len(failed_tests)) + ", SKIPPED: " + str(skipped_count))
        
    return res


def check_file_exists(name):
    if not os.path.exists(name):
        fatal_error("Required file '" + name + "' does not exist")

def run_tests(install_dirs: Dict, argv=[]) -> int:
    opts = process_opts()

    if opts.mcell_build_path_override:
        install_dirs[REPO_NAME_MCELL] = opts.mcell_build_path_override 

    if opts.mcell_build_path_override:
        install_dirs[REPO_NAME_CELLBLENDER] = opts.cellblender_build_path_override 

    # FIXME: use arguments directly to initialize ToolPaths    
    tool_paths = ToolPaths(install_dirs)
    log(str(tool_paths))
    
    results = collect_and_run_tests(tool_paths, opts)
    ec = report_results(results)
    return ec


if __name__ == '__main__':
    ec = run_tests({}, sys.argv)
    sys.exit(ec)
    

