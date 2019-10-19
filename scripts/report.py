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

import os
import sys


def report_results_to_output(results: Dict) -> int:
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


def report_results_as_html_and_collect_fails(results: Dict):
    
    # generate html with tests that failed
    # html file name: release, time, branch, ...?
    
    # collect fails 
    
    # pack it all together and return the name of the file
    
    
    # on the server side, there will be a generator that 
    # goes through a directory and makes the test results available for download
    # use frames
    # the generator can be run by jenkins? 
    
    
    
    