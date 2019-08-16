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
"""

import os
import sys
import subprocess
import multiprocessing 
import re
import shutil
from threading import Timer

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, 'scripts'))

from test_settings import *
from test_utils import ToolPaths, report_test_error, report_test_success

# import tester classes
from tester_mdl import TesterMdl

sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))

from utils import run, log

class TestSetInfo:
    def __init__(self, test_set_dir, tester_class):
        self.test_set_dir = test_set_dir
        self.tester_class = tester_class

# we are only adding the specific test directory
class TestInfo(TestSetInfo):
    def __init__(self, test_set_dir, tester_class, test_dir):
        self.test_dir = test_dir
        super(TestInfo, self).__init__(test_set_dir, tester_class)

    def __repr__(self):
        return '[' + str(self.tester_class) + ']:' + os.path.join(self.test_set_dir, self.test_dir)

# list of test directories with classes that are designed to test them
TEST_SET_DIRS = [
    TestSetInfo('tests_mdl', TesterMdl)
]


# returns a list of TestInfo objects - TODO
def get_test_dirs(test_set_info):
    res = []
    test_set_full_path = os.path.join(THIS_DIR, test_set_info.test_set_dir)
    print("Looking for tests in " + test_set_full_path)
    files = os.listdir(test_set_full_path)
    for name in files:
        name_w_dir = os.path.join(test_set_full_path, name)
        if os.path.isdir(name_w_dir):
            res.append( TestInfo(test_set_info.test_set_dir, test_set_info.tester_class, name_w_dir) )
    return res
   
    
def run_single_test(test_info, tool_paths):    
    test_obj = test_info.tester_class(os.path.join(test_info.test_set_dir, test_info.test_dir), tool_paths)
    test_obj.test()
    

def collect_and_run_tests(tool_paths, test_pattern, parallel):
    
    test_infos = []
    for test_set in TEST_SET_DIRS:
        test_infos += get_test_dirs(test_set)
    

    #test_infos.sort(key = lambda x: x.test_set_dir)
    test_infos.sort(key = lambda x: (x.test_set_dir + x.test_dir))
    
    results = {}

    filtered_test_infos = []
    for info in test_infos:
        if not test_pattern or re.search(test_pattern, info.test_dir):
            filtered_test_infos.append(info)

    log("Tests to be run:")
    for info in filtered_test_infos:
        log(str(info))

    work_dir = os.getcwd()
    if not parallel:
        for info in filtered_test_infos:
            print("Testing " + info.test_dir)
            res = run_single_test(info, tool_paths)
            results[test_set_dir] = res
            os.chdir(work_dir)  # just to be sure, let's fix cwd
    else:
        # Set up the parallel task pool to use all available processors
        count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=count)
 
        # Run the jobs
        result_values = pool.map(run_single_test, filtered_test_infos)
        # TODO: the first item must be a list of names
        results = dict(zip(filtered_test_infos, result_values))

    return results


def report_results(results):
    print('\n**** RESULTS ****')
    passed = 0
    failed = 0
    skipped = 0
    for key, value in results.items():
        print(RESULT_NAMES[value] + ": " + os.path.basename(key))
        if value == PASSED:
            passed += 1
        elif value == FAILED_MCELL or value == FAILED_DIFF:
            failed += 1
        elif value == SKIPPED:
            skipped += 1
        else:
            fatal_error('Invalid test result value ' + str(value))
           
    if failed != 0:
        print('\n!! THERE WERE ERRORS !!')
    else:
        print('\n-- SUCCESS --')


def run_tests(install_dirs, argv=[]):
    tool_paths = ToolPaths(install_dirs)
    log(str(tool_paths))
    
    test_pattern = ''
    parallel = False
    if len(argv) == 2:
        if argv[1] == 'sequential':
            parallel = False
        else:
            test_pattern = argv[1]
        
    results = collect_and_run_tests(tool_paths, test_pattern, parallel)
    report_results(results)


if __name__ == '__main__':
    run_tests({}, sys.argv)
    

