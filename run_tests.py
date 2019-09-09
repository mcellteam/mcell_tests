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
"""

import os
import sys
import subprocess
import multiprocessing
import itertools 
import re
import shutil
from datetime import datetime
from threading import Timer
from typing import List, Dict


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, 'scripts'))

from test_settings import *
from test_utils import ToolPaths, report_test_error, report_test_success

# import tester classes
from tester_mdl import TesterMdl
from tester_datamodel import TesterDataModel
from tester_nutmeg import TesterNutmeg

sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))

from utils import run, log, fatal_error


class TestSetInfo:
    def __init__(self, category: str, test_set_name: str, tester_class: str):
        self.category = category  # e.g. tests or examples
        self.test_set_name = test_set_name  # e.g. nutmeg_positive
        self.tester_class = tester_class  # class derived from TesterBase


# we are only adding the specific test directory
class TestInfo(TestSetInfo):
    def __init__(self, test_set_info: TestSetInfo, test_path: str):
        self.test_path = test_path  # full path to the test directory
        super(TestInfo, self).__init__(test_set_info.category, test_set_info.test_set_name, test_set_info.tester_class)

    def __repr__(self):
        return '[' + str(self.tester_class) + ']:' + os.path.join(self.test_path)

    def get_full_name(self):
        # not using os.path.join because the name must be identical on every system
        return self.category + '/' + self.test_set_name + '/' + os.path.basename(self.test_path)


# list of test directories with classes that are designed to test them
TEST_SET_DIRS = [
    #TestSetInfo('tests', 'mdl', TesterMdl),
    #TestSetInfo('examples', 'datamodel', TesterDataModel),
    #TestSetInfo('tests', 'nutmeg_positive', TesterNutmeg),
    TestSetInfo('tests', 'nutmeg_negative', TesterNutmeg)
]


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
    test_obj = test_info.tester_class(test_info.test_path, tool_paths)
    res = test_obj.test()
    log("FINISHED: " + test_info.get_full_name() + " at " + datetime.now().strftime('%H:%M:%S'))
    return res
    
    
def collect_and_run_tests(tool_paths: ToolPaths, test_pattern: str, parallel: bool) -> Dict:
    test_infos = []
    for test_set in TEST_SET_DIRS:
        test_infos += get_test_dirs(test_set)

    filtered_test_infos = []
    for info in test_infos:
        if not test_pattern or re.search(test_pattern, info.test_path):
            filtered_test_infos.append(info)

    filtered_test_infos.sort(key=lambda x: x.get_full_name())

    log("Tests to be run:")
    for info in filtered_test_infos:
        log(str(info))

    results = {}
    work_dir = os.getcwd()
    if not parallel:
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


def report_results(results: Dict) -> None:
    print("\n**** RESULTS ****")
    passed = 0
    failed = 0
    skipped = 0
    for key, value in results.items():
        print(RESULT_NAMES[value] + ": " + str(key))
        if value == PASSED:
            passed += 1
        elif value in [FAILED_MCELL, FAILED_DIFF, FAILED_DM_TO_MDL_CONVERSION, FAILED_NUTMEG_SPEC]:
            failed += 1
        elif value == SKIPPED:
            skipped += 1
        else:
            fatal_error("Invalid test result value " + str(value))
           
    if failed != 0:
        log("\n!! THERE WERE ERRORS !!")
    else:
        log("\n-- SUCCESS --")


def run_tests(install_dirs: Dict, argv=[]) -> None:
    tool_paths = ToolPaths(install_dirs)
    log(str(tool_paths))
    
    test_pattern = ''
    parallel = True
    if len(argv) == 2 or len(argv) == 3:
        if argv[1] == 'sequential':
            parallel = False
            if len(argv) == 3:
                test_pattern = argv[2]
        else:
            test_pattern = argv[1]
    
    results = collect_and_run_tests(tool_paths, test_pattern, parallel)
    report_results(results)


if __name__ == '__main__':
    run_tests({}, sys.argv)
    

