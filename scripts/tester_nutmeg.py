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
This module contains functions to check tests in tests_mdl.
"""

import os
import sys
import shutil
import toml
import re
import subprocess
from typing import List, Dict

import data_output_diff
from test_settings import *
from tester_base import TesterBase
from test_utils import ToolPaths, report_test_error, report_test_success, replace_in_file

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error


TEST_DESCRIPTION_FILE = 'test_description.toml'

TIMEOUT_EXIT_CODE = 126

LOG_FILE_NAME = 'mcell.log'
STDOUT_FILE_NAME = 'mcell_stdout.log'
STDERR_FILE_NAME = 'mcell_stderr.log'
NUTMEG_LOG_FILE_NAME = 'nutmeg.log'

# ignoring the patterns in original nutmeg files
STDOUT_FILE_NAME_FROM_TOML = 'run_%d.0.log'
STDERR_FILE_NAME_FROM_TOML = 'err_%d.0.log'


KEY_RUN = 'run'

KEY_COMMAND_LINE_OPTIONS = 'commandlineOpts'
KEY_MDL_FILES = 'mdlfiles'

SUBKEYS_RUN = [KEY_COMMAND_LINE_OPTIONS, KEY_MDL_FILES]


KEY_CHECKS = 'checks'

KEY_TEST_TYPE = 'testType'
KEY_FILE_NAMES = 'dataFile' 
KEY_DATA_FILE = 'dataFile' 
KEY_NUM_MATCHES = 'numMatches' # only 1 supported
KEY_MATCH_PATTERN = 'matchPattern'
KEY_HAVE_HEADER = 'haveHeader' # ignored
KEY_REFERENCE_FILE = 'referenceFile'
KEY_COUNT_MINIMUM = 'countMinimum'
KEY_COUNT_MAXIMUM = 'countMaximum'
KEY_MIN_TIME = 'minTime'
KEY_MAX_TIME = 'maxTime'

SUBKEYS_CHECKS = [
    KEY_FILE_NAMES, KEY_DATA_FILE, KEY_HAVE_HEADER, 
    KEY_REFERENCE_FILE, KEY_TEST_TYPE, 
    KEY_COUNT_MINIMUM, KEY_COUNT_MAXIMUM,
    KEY_MIN_TIME, KEY_MAX_TIME,
    KEY_NUM_MATCHES, KEY_MATCH_PATTERN
]

TEST_TYPE_INVALID = -1
TEST_TYPE_CHECK_SUCCESS = 0
TEST_TYPE_CHECK_EXIT_CODE = 1

TEST_TYPE_DIFF_FILE_CONTENT = 10  # exact match with a reference file, same as original DIFF_FILE_CONTENT
TEST_TYPE_FDIFF_FILE_CONTENT = 11  # match with allowed tolerance  

TEST_TYPE_ZERO_COUNTS = 20
TEST_TYPE_POSITIVE_OR_ZERO_COUNTS = 21
TEST_TYPE_POSITIVE_COUNTS = 22
TEST_TYPE_COUNT_MINMAX = 23

TEST_TYPE_CHECK_NONEMPTY_FILES = 30
TEST_TYPE_CHECK_EMPTY_FILES = 31

TEST_TYPE_FILE_MATCH_PATTERN = 40


TEST_TYPE_UPDATE_REFERENCE = 50


TEST_TYPE_ID_TO_NAME = {
    TEST_TYPE_INVALID: 'INVALID',
    TEST_TYPE_CHECK_SUCCESS: 'CHECK_SUCCESS',
    TEST_TYPE_CHECK_EXIT_CODE: 'CHECK_EXIT_CODE',

    TEST_TYPE_DIFF_FILE_CONTENT: 'DIFF_FILE_CONTENT',
    TEST_TYPE_FDIFF_FILE_CONTENT: 'FDIFF_FILE_CONTENT',
    
    TEST_TYPE_ZERO_COUNTS: 'ZERO_COUNTS',
    TEST_TYPE_POSITIVE_OR_ZERO_COUNTS: 'POSITIVE_OR_ZERO_COUNTS',
    TEST_TYPE_POSITIVE_COUNTS: 'POSITIVE_COUNTS',
    TEST_TYPE_COUNT_MINMAX: 'COUNT_MINMAX',

    TEST_TYPE_CHECK_NONEMPTY_FILES: 'CHECK_NONEMPTY_FILES',
    TEST_TYPE_CHECK_EMPTY_FILES: 'CHECK_EMPTY_FILES',

    TEST_TYPE_FILE_MATCH_PATTERN: 'FILE_MATCH_PATTERN',
    
    TEST_TYPE_UPDATE_REFERENCE: 'COUNT_CONSTRAINTS'
}

TEST_TYPE_NAME_TO_ID = {y: x for x,y in TEST_TYPE_ID_TO_NAME.items()}
    

class CheckInfo:
    def __init__(self):
        self.test_type = TEST_TYPE_INVALID
        self.data_file = ''
        self.count_minimum = None  # for TEST_TYPE_COUNT_MINMAX
        self.count_maximum = None  # for TEST_TYPE_COUNT_MINMAX
        self.min_time = None  # optional for TEST_TYPE_COUNT_MINMAX
        self.max_time = None  # optional for TEST_TYPE_COUNT_MINMAX
        self.match_pattern = None

    def __repr__(self):
        attrs = vars(self)
        return ", ".join("%s: %s" % item for item in attrs.items())


class RunInfo:
    def __init__(self):
        self.mdlfile = ''
        self.command_line_options = []


class TestDescription:
    def __init__(self):
        self.run_info = None
        self.check_infos = []


class TestDescriptionParser:
    def __init__(self, test_src_path: str):
        self.test_src_path = test_src_path

    def parse_error(self, msg: str):
        log(msg + " While parsing " + os.path.join(self.test_src_path, TEST_DESCRIPTION_FILE) + ".")

    def parse_warning(self, msg: str):
        log(msg + " While parsing " + os.path.join(self.test_src_path, TEST_DESCRIPTION_FILE) + ".")

    def get_dict_value(self, d: Dict, key: str) -> str:
        if key not in d:
            self.parse_error("Required field '" + key + "' not found.")
        res = d[key]
        return res
    
    def check_supported_keys(self, d: Dict, keys: List[str]) -> None:
        for key in d.keys():
            if key not in keys:
                self.parse_error("Unknown field '" + key + "' in " + str(d) + ".")
    
    def parse_run_info(self, top_dict: Dict) -> RunInfo:
        run_dict = self.get_dict_value(top_dict, KEY_RUN)
        self.check_supported_keys(run_dict, SUBKEYS_RUN)
        
        res = RunInfo()
        
        mdlfiles = self.get_dict_value(run_dict, KEY_MDL_FILES)
        if len(mdlfiles) != 1:
            self.parse_error("There can be just one mdl file (key mdlfiles).")
        res.mdlfile = mdlfiles[0]  
        
        if KEY_COMMAND_LINE_OPTIONS in run_dict:
            res.command_line_options = run_dict[KEY_COMMAND_LINE_OPTIONS]
        return res
        
    def get_test_type(self, value: str) -> int:
        if value not in TEST_TYPE_NAME_TO_ID:
            self.parse_error("Value of testType '" + value + "' is not supported.")
        return TEST_TYPE_NAME_TO_ID[value]
        
    def parse_check_info(self, check_dict: Dict) -> CheckInfo:
        res = CheckInfo()
        self.check_supported_keys(check_dict, SUBKEYS_CHECKS)
        
        test_type_str = self.get_dict_value(check_dict, KEY_TEST_TYPE)
        res.test_type = self.get_test_type(test_type_str)
        
        if res.test_type in [TEST_TYPE_DIFF_FILE_CONTENT, TEST_TYPE_FDIFF_FILE_CONTENT]:

            res.data_file = self.get_dict_value(check_dict, KEY_DATA_FILE)
            
            if KEY_HAVE_HEADER in check_dict:
                self.parse_warning("Key " + KEY_HAVE_HEADER + " is ignored")
            if KEY_REFERENCE_FILE in check_dict:
                self.parse_warning("Key " + KEY_REFERENCE_FILE + " is ignored")
                
        elif res.test_type in [TEST_TYPE_ZERO_COUNTS, TEST_TYPE_POSITIVE_OR_ZERO_COUNTS, 
                               TEST_TYPE_POSITIVE_COUNTS, TEST_TYPE_COUNT_MINMAX]:
            res.data_file = self.get_dict_value(check_dict, KEY_DATA_FILE)

            if KEY_COUNT_MINIMUM in check_dict:
                min_list = self.get_dict_value(check_dict, KEY_COUNT_MINIMUM)
                if len(min_list) != 1:
                    self.parse_error("Key " + KEY_COUNT_MINIMUM + " must contain a list with a single value")
                    return None
                res.count_minimum = min_list[0]

            if KEY_COUNT_MAXIMUM in check_dict:
                max_list = check_dict[KEY_COUNT_MAXIMUM]
                if len(max_list) != 1:
                    self.parse_error("Key " + KEY_COUNT_MINIMUM + " must contain a list with a single value")
                    return None
                res.count_maximum = max_list[0]
            
            if KEY_MIN_TIME in check_dict:
                res.min_time = check_dict[KEY_MIN_TIME]
            if KEY_MAX_TIME in check_dict:
                res.max_time = check_dict[KEY_MAX_TIME]
                
            if KEY_HAVE_HEADER in check_dict:
                self.parse_warning("Key " + KEY_HAVE_HEADER + " is ignored")
                
        elif res.test_type == TEST_TYPE_FILE_MATCH_PATTERN:
            data_file_from_toml = self.get_dict_value(check_dict, KEY_DATA_FILE)
            if data_file_from_toml == STDOUT_FILE_NAME_FROM_TOML:
                res.data_file = STDOUT_FILE_NAME
            elif data_file_from_toml == STDERR_FILE_NAME_FROM_TOML:
                res.data_file = STDERR_FILE_NAME
            else:
                self.parse_error(
                    "Value for " + KEY_DATA_FILE + " FILE_MATCH_PATTERN must be either " + 
                    STDOUT_FILE_NAME_FROM_TOML + " or " + STDERR_FILE_NAME_FROM_TOML)
                return None
            
            res.match_pattern = self.get_dict_value(check_dict, KEY_MATCH_PATTERN)
            if KEY_NUM_MATCHES in check_dict:
                num_matches = self.get_dict_value(check_dict, KEY_NUM_MATCHES)
                if num_matches != 1:
                    self.parse_error("Value for " + KEY_NUM_MATCHES + " must be only 1.")
                    return None
            
        elif res.test_type == TEST_TYPE_CHECK_SUCCESS:
            # no other attributesw are relevant
            pass
        else:
            self.parse_error("Check type '" + test_type_str + "' is not supported yet.")
            res.test_type = TEST_TYPE_UPDATE_REFERENCE
            res.data_file = self.get_dict_value(check_dict, KEY_DATA_FILE)
        
        return res
    
    def parse_test_description(self) -> TestDescription:
        test_description = os.path.join(self.test_src_path, TEST_DESCRIPTION_FILE)
        if not os.path.exists(test_description):
            self.parse_error("Could not open nutmeg test specification file '" + test_description + "'.")
            return None
        
        top_dict = toml.load(test_description)
        
        res = TestDescription()
        res.run_info = self.parse_run_info(top_dict)
        
        checks_list = self.get_dict_value(top_dict, KEY_CHECKS)
        if not checks_list:
            self.parse_error("There must be at least one check.")
        for check in checks_list: 
            info = self.parse_check_info(check)
            if info is None:
                return None
            res.check_infos.append(info)
            
        return res
  

class TesterNutmeg(TesterBase):
    def __init___(self, test_src_path: str, tool_paths: ToolPaths):
        super(TesterNutmeg, self).__init__(test_src_path, tool_paths)

    def check_prerequisites(self) -> None:
        if not os.path.exists(self.tool_paths.mcell_binary):
            fatal_error("Could not find executable '" + self.tool_paths.mcell_binary + ".")

    def nutmeg_log(self, msg, test_type) -> None:
        full_msg = TEST_TYPE_ID_TO_NAME[test_type] + ": " + msg
        log_fname = os.path.join(self.test_work_path, NUTMEG_LOG_FILE_NAME)
        with open(log_fname, "a+") as fout:
            fout.write(full_msg + "\n")
        log(self.test_name + ": " + full_msg)

    # returns exit code returned by mcell
    def run_mcell_for_nutmeg(self, run_info: RunInfo) -> int:
        fout = open(os.path.join(self.test_work_path, STDOUT_FILE_NAME), "w")
        ferr = open(os.path.join(self.test_work_path, STDERR_FILE_NAME), "w")
        flog = open(os.path.join(self.test_work_path, LOG_FILE_NAME), "w")

        mcell_cmd = [self.tool_paths.mcell_binary]
        mcell_cmd += run_info.command_line_options
        mcell_cmd.append(os.path.join(self.test_src_path, run_info.mdlfile))
        flog.write(str.join(" ", mcell_cmd) + " (" + str(mcell_cmd) + ")\ncwd: " + self.test_work_path + "\n")

        try:
            run_res = subprocess.run(mcell_cmd, stdout=fout, stderr=ferr, cwd=self.test_work_path, timeout=MCELL_TIMEOUT)
            mcell_ec = run_res.returncode

        except subprocess.TimeoutExpired:
            flog.write("Command timeouted after " + str(MCELL_TIMEOUT) + " seconds.")
            mcell_ec = TIMEOUT_EXIT_CODE

        fout.close()
        ferr.close()
        flog.close()

        return mcell_ec
    
    def report_check_counts_error(self, line: str, check: CheckInfo):
        minmax_str = ""
        if check.test_type == TEST_TYPE_COUNT_MINMAX:
            minmax_str = "min: " + str(check.count_minimum) + ", max: " + str(check.count_maximum)  
        
        self.nutmeg_log(
            "Count check failed for line '" + line + "' " + minmax_str, check.test_type)
        

    def check_counts(self, check: CheckInfo) -> int:
        data_file_path = os.path.join(self.test_work_path, check.data_file)
        # expecting that the data file contains only two columns: iteration and value
        res = PASSED
        try:
            with open(data_file_path, "r") as fin:
                for line in fin:
                    vals = line.split(' ')
                    if vals[0] == '#':
                        continue  # header
                    time = float(vals[0])
                    val = int(vals[1])

                    time_constraint_valid = True
                    if check.min_time is not None: 
                        time_constraint_valid = time >= check.min_time

                    if check.max_time is not None:
                        time_constraint_valid = time_constraint_valid and time <= check.max_time
                    
                    if check.test_type == TEST_TYPE_ZERO_COUNTS:
                        if time_constraint_valid and val != 0:
                            res = FAILED_NUTMEG_SPEC
                    elif check.test_type == TEST_TYPE_POSITIVE_OR_ZERO_COUNTS:
                        if time_constraint_valid and val < 0:
                            res = FAILED_NUTMEG_SPEC
                    elif check.test_type == TEST_TYPE_POSITIVE_COUNTS:
                        if time_constraint_valid and val <= 0:
                            res = FAILED_NUTMEG_SPEC
                    elif check.test_type == TEST_TYPE_COUNT_MINMAX:
                        if time_constraint_valid and \
                            ((check.count_minimum is not None and val < check.count_minimum) or \
                             (check.count_maximum is not None and val > check.count_maximum)):
                            res = FAILED_NUTMEG_SPEC
                    else:
                        fatal_error("Unknown test type in check_counts: " + str(check.test_type))\
                        
                    if res != PASSED:
                        self.report_check_counts_error(line, check)
                        return res
                        
                        
        except Exception as e:
            self.nutmeg_log(
                "Failed while parsing data file '" + data_file_path + "', exception " + str(e.args), check.test_type)
            return FAILED_NUTMEG_SPEC

        return PASSED

    def check_match_pattern(self, check: CheckInfo) -> int:
        data_file_path = os.path.join(self.test_work_path, check.data_file)
        try:   
            with open(data_file_path, "r") as fin:
                matcher = re.compile(check.match_pattern)
                for line in fin:
                    if matcher.search(line):
                        return PASSED
                
        except Exception as e:
            self.nutmeg_log(
                "Failed while parsing data file '" + data_file_path + "', exception " + str(e.args), check.test_type)
            return FAILED_NUTMEG_SPEC

        return FAILED_NUTMEG_SPEC

    def run_check(self, check: CheckInfo, mcell_ec: int) -> int:

        res = FAILED_DIFF
        if check.test_type in [TEST_TYPE_DIFF_FILE_CONTENT, TEST_TYPE_FDIFF_FILE_CONTENT]:
            # exact file compare
            res = data_output_diff.compare_data_output_files(
                os.path.join('..', self.test_src_path, REF_NUTMEG_DATA_DIR, check.data_file),
                os.path.join(self.test_work_path, check.data_file),
                exact=(check.test_type == TEST_TYPE_DIFF_FILE_CONTENT) )
            self.nutmeg_log("Comparison result of '" + check.data_file + "': " + RESULT_NAMES[res], check.test_type)

        elif check.test_type in [TEST_TYPE_ZERO_COUNTS, TEST_TYPE_POSITIVE_OR_ZERO_COUNTS, 
                                 TEST_TYPE_POSITIVE_COUNTS, TEST_TYPE_COUNT_MINMAX]:
            res = self.check_counts(check)
            self.nutmeg_log("Comparison result of '" + check.data_file + "': " + RESULT_NAMES[res], check.test_type)
                
        elif check.test_type == TEST_TYPE_CHECK_SUCCESS:
            if mcell_ec == 0:
                self.nutmeg_log("Mcell exit code is 0 as expected.", check.test_type)
                res = PASSED
            else:
                self.nutmeg_log("Expected exit code 0 but mcell returned " + str(mcell_ec), check.test_type)

        elif check.test_type == TEST_TYPE_FILE_MATCH_PATTERN:
            res = self.check_match_pattern(check)
            self.nutmeg_log("Finding pattern " + check.match_pattern + " in " + check.data_file + "': " + RESULT_NAMES[res], check.test_type)

        elif check.test_type == TEST_TYPE_UPDATE_REFERENCE:
            ref_dir = os.path.join(self.test_src_path, REF_NUTMEG_DATA_DIR)
            if not os.path.exists(ref_dir):
                os.mkdir(ref_dir)
            ref_file = os.path.join(self.test_work_path, check.data_file)
            self.nutmeg_log("Updating contents in " + ref_dir + " with " + ref_file + ".", check.test_type)
            shutil.copy(ref_file, ref_dir)
            res = NUTMEG_UPDATED_REFERENCE
        else:
            fatal_error("Unexpected check type " + TEST_TYPE_ID_TO_NAME[check.test_type])

        return res

    def run_and_validate_test(self, test_description: TestDescription) -> int:
        # 1) run mcell while capturing std and err output to different files
        #    non-zero exit code might be an expected result
        mcell_ec = self.run_mcell_for_nutmeg(test_description.run_info)

        # 2) run all checks
        for check in test_description.check_infos:
            res = self.run_check(check, mcell_ec)
            if res != PASSED:
                return res

        return PASSED

    def test(self) -> int:
        self.check_prerequisites()

        if self.should_be_skipped():
            return SKIPPED

        self.clean_and_create_work_dir()
        
        # transform the result ito something more readable or keep as dictionary?
        parser = TestDescriptionParser(self.test_src_path)
        test_description = parser.parse_test_description()
        if test_description is None:
            return FAILED_NUTMEG_SPEC        

        res = self.run_and_validate_test(test_description)
         
        return res
