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
import platform
from typing import List, Dict

import data_output_diff
from test_settings import *
from tester_base import TesterBase
from test_utils import ToolPaths, replace_in_file

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, execute, log, fatal_error

# set to True for additoinal info being printed onto terminal 
NUTMEG_VERBOSE = False

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
KEY_JSON_FILE = 'jsonFile'
KEY_MAX_MEMORY = 'maxMemory'

SUBKEYS_RUN = [KEY_COMMAND_LINE_OPTIONS, KEY_MDL_FILES, KEY_JSON_FILE, KEY_MAX_MEMORY]


KEY_CHECKS = 'checks'

KEY_TEST_TYPE = 'testType'
KEY_FILE_NAMES = 'fileNames' 
KEY_DATA_FILE = 'dataFile' 
KEY_NUM_MATCHES = 'numMatches' # only 1 supported
KEY_MATCH_PATTERN = 'matchPattern'
KEY_HAVE_HEADER = 'haveHeader' # ignored
KEY_REFERENCE_FILE = 'referenceFile'
KEY_COUNT_MINIMUM = 'countMinimum'
KEY_COUNT_MAXIMUM = 'countMaximum'
KEY_MIN_TIME = 'minTime'
KEY_MAX_TIME = 'maxTime'
KEY_DESCRIPTION = 'description'

SUBKEYS_CHECKS = [
    KEY_FILE_NAMES, KEY_DATA_FILE, KEY_HAVE_HEADER, 
    KEY_REFERENCE_FILE, KEY_TEST_TYPE, 
    KEY_COUNT_MINIMUM, KEY_COUNT_MAXIMUM,
    KEY_MIN_TIME, KEY_MAX_TIME,
    KEY_NUM_MATCHES, KEY_MATCH_PATTERN,
    KEY_DESCRIPTION
]

KEY_INCLUDES = 'includes'
VALUE_INCLUDES_EXIT_CODE_1 = 'exit_code_1'


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
        self.data_file = None
        self.count_minimum = None  # for TEST_TYPE_COUNT_MINMAX
        self.count_maximum = None  # for TEST_TYPE_COUNT_MINMAX
        self.min_time = None  # optional for TEST_TYPE_COUNT_MINMAX
        self.max_time = None  # optional for TEST_TYPE_COUNT_MINMAX
        self.match_pattern = None
        self.exit_code = None # for TEST_TYPE_CHECK_EXIT_CODE

    def __repr__(self):
        attrs = vars(self)
        return ", ".join("%s: %s" % item for item in attrs.items())


class RunInfo:
    def __init__(self):
        self.mdl_files = []
        self.json_file = None
        self.command_line_options = []
        self.max_memory = None


class TestDescription:
    def __init__(self):
        self.run_info = None
        self.check_infos = []


class TestDescriptionParser:
    def __init__(self, test_src_path: str):
        self.test_src_path = test_src_path

    def parse_error(self, msg: str):
        log(msg + " while parsing " + os.path.join(self.test_src_path, TEST_DESCRIPTION_FILE) + ".")

    def parse_warning(self, msg: str):
        log(msg + " while parsing " + os.path.join(self.test_src_path, TEST_DESCRIPTION_FILE) + ".")

    def get_dict_value(self, d: Dict, key: str) -> str:
        if key not in d:
            self.parse_error("Required field '" + key + "' not found.")
        res = d[key]
        return res
    
    def check_supported_keys(self, d: Dict, keys: List[str]) -> bool:
        for key in d.keys():
            if key not in keys:
                self.parse_error("Unknown field '" + key + "' in " + str(d) + ".")
                return False
        return True
    
    def parse_run_info(self, top_dict: Dict) -> RunInfo:
        run_dict = self.get_dict_value(top_dict, KEY_RUN)
        ok = self.check_supported_keys(run_dict, SUBKEYS_RUN)
        if not ok:
            return None
        
        res = RunInfo()
        
        if KEY_MDL_FILES in run_dict:
            mdlfiles = run_dict[KEY_MDL_FILES]
            if len(mdlfiles) < 1:
                self.parse_error("There has to be at least one mdl file (key '" + KEY_MDL_FILES + "').")
            res.mdl_files = mdlfiles  

        if KEY_JSON_FILE in run_dict:
            res.json_file = run_dict[KEY_JSON_FILE]

        if KEY_MAX_MEMORY in run_dict:
            res.max_memory = run_dict[KEY_MAX_MEMORY]
            
            
        if res.mdl_files and res.json_file:
            self.parse_error("Only one of '" + KEY_MDL_FILES + "' and '" + KEY_JSON_FILE + "' can be specified.")
        if not res.mdl_files and not res.json_file:
            self.parse_error("One of '" + KEY_MDL_FILES + "' and '" + KEY_JSON_FILE + "' must be specified.")
        
        if KEY_COMMAND_LINE_OPTIONS in run_dict:
            res.command_line_options = run_dict[KEY_COMMAND_LINE_OPTIONS]
        return res
        
    def get_test_type(self, value: str) -> int:
        if value not in TEST_TYPE_NAME_TO_ID:
            self.parse_error("Value of testType '" + value + "' is not supported.")
        return TEST_TYPE_NAME_TO_ID[value]
    
    def get_data_file_name(self, check_dict: Dict) -> str:
        if KEY_DATA_FILE in check_dict:
            data_file_from_toml = check_dict[KEY_DATA_FILE]
            
        elif KEY_FILE_NAMES in check_dict:
            file_names = check_dict[KEY_FILE_NAMES]
            if len(file_names) != 1:
                self.parse_error("There can be just one file in fileNames.")
            data_file_from_toml = file_names[0]
            
        else:
            self.parse_error(
                "Expected either '" + KEY_DATA_FILE + 
                "' or '" + KEY_FILE_NAMES + "' key to be present.")
            
        if data_file_from_toml == STDOUT_FILE_NAME_FROM_TOML:
            return STDOUT_FILE_NAME
        elif data_file_from_toml == STDERR_FILE_NAME_FROM_TOML:
            return STDERR_FILE_NAME
        else:
            return data_file_from_toml 
        
    def parse_check_info(self, check_dict: Dict) -> CheckInfo:
        res = CheckInfo()
        ok = self.check_supported_keys(check_dict, SUBKEYS_CHECKS)
        if not ok:
            return None
        
        test_type_str = self.get_dict_value(check_dict, KEY_TEST_TYPE)
        res.test_type = self.get_test_type(test_type_str)
        
        if res.test_type in [TEST_TYPE_DIFF_FILE_CONTENT, TEST_TYPE_FDIFF_FILE_CONTENT]:

            res.data_file = self.get_dict_value(check_dict, KEY_DATA_FILE)
            
            #if KEY_HAVE_HEADER in check_dict:
            #    self.parse_warning("Key " + KEY_HAVE_HEADER + " is ignored")
            #if KEY_REFERENCE_FILE in check_dict:
            #    self.parse_warning("Key " + KEY_REFERENCE_FILE + " is ignored")
                
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
                
            #if KEY_HAVE_HEADER in check_dict:
            #    self.parse_warning("Key " + KEY_HAVE_HEADER + " is ignored")
                
        elif res.test_type == TEST_TYPE_FILE_MATCH_PATTERN:
            res.data_file = self.get_data_file_name(check_dict)
            
            res.match_pattern = self.get_dict_value(check_dict, KEY_MATCH_PATTERN)
            if KEY_NUM_MATCHES in check_dict:
                num_matches = self.get_dict_value(check_dict, KEY_NUM_MATCHES)
                if num_matches != 1:
                    self.parse_error("Value for " + KEY_NUM_MATCHES + " must be only 1.")
                    return None
                
        elif res.test_type in [TEST_TYPE_CHECK_EMPTY_FILES, TEST_TYPE_CHECK_NONEMPTY_FILES]:
            res.data_file = self.get_data_file_name(check_dict)         
        
        elif res.test_type == TEST_TYPE_CHECK_SUCCESS:
            # no other attributes are relevant
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

        # general run info        
        res = TestDescription()
        res.run_info = self.parse_run_info(top_dict)
        if res.run_info is None:
            return None
        
        # checks
        if KEY_CHECKS in top_dict:
            checks_list = self.get_dict_value(top_dict, KEY_CHECKS)
            for check in checks_list: 
                info = self.parse_check_info(check)
                if info is None:
                    return None
                res.check_infos.append(info)
            
           
        # there can be also line  'includes = ["exit_code_1"]' 
        if KEY_INCLUDES in top_dict:
            if top_dict[KEY_INCLUDES] == VALUE_INCLUDES_EXIT_CODE_1:
                exit_1 = CheckInfo()
                exit_1.test_type = TEST_TYPE_CHECK_EXIT_CODE
                exit_1.exit_code = 1
                res.check_infos.append(exit_1) 
            
        return res
  

class TesterNutmeg(TesterBase):
    def __init___(self, test_src_path: str, args: List[str], tool_paths: ToolPaths):
        super(TesterNutmeg, self).__init__(test_src_path, args, tool_paths)

    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterBase.check_prerequisites(tool_paths) 
        
    def nutmeg_log(self, msg, test_type) -> None:
        full_msg = TEST_TYPE_ID_TO_NAME[test_type] + ": " + msg
        log_fname = os.path.join(self.test_work_path, NUTMEG_LOG_FILE_NAME)
        with open(log_fname, "a+") as fout:
            fout.write(full_msg + "\n")
            
        if NUTMEG_VERBOSE:
            log(self.test_name + ": " + full_msg)

    # returns exit code returned by mcell
    def run_mcell_for_nutmeg(self, run_info: RunInfo) -> int:
        fout = open(os.path.join(self.test_work_path, STDOUT_FILE_NAME), "w")
        ferr = open(os.path.join(self.test_work_path, STDERR_FILE_NAME), "w")
        flog = open(os.path.join(self.test_work_path, LOG_FILE_NAME), "w")

        
        for mdl_file in run_info.mdl_files:
            mcell_cmd = [self.tool_paths.mcell_binary]
            mcell_cmd += run_info.command_line_options

            if not run_info.json_file:
                # mdl_file is in the test directory
                mcell_cmd.append(os.path.join(self.test_src_path, mdl_file))
            else:
                # mdl_file is in the work directory
                mcell_cmd.append(os.path.join(self.test_work_path, mdl_file))
            
            flog.write(str.join(" ", mcell_cmd) + " (" + str(mcell_cmd) + ")\ncwd: " + self.test_work_path + "\n")
    
            # should we enable mcellr mode?
            mdlr_rules_file = os.path.join(self.test_work_path, MAIN_MDLR_RULES_FILE)
            if os.path.exists(mdlr_rules_file):
                mcell_cmd += [ '-r', mdlr_rules_file ]
    
            try:
                shell = False
                if run_info.max_memory:    
                    shell = True
                    if 'Windows' in platform.system():
                        log("Warning: Max memory testing is not supported on Windows for test definition '" + run_info.json_file + "', test is run without this check.")
                    else:
                        # insert call to ulimit in front
                        mcell_cmd = 'ulimit -sv ' + str(run_info.max_memory * 1000) + ';' + str.join(" ", mcell_cmd)  
                
                run_res = subprocess.run(
                    mcell_cmd, shell=shell, 
                    stdout=fout, stderr=ferr, cwd=self.test_work_path, timeout=MCELL_TIMEOUT)
                mcell_ec = run_res.returncode
                if mcell_ec != 0:
                    break
    
            except subprocess.TimeoutExpired:
                flog.write("Command timeouted after " + str(MCELL_TIMEOUT) + " seconds.")
                mcell_ec = TIMEOUT_EXIT_CODE
                break

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
                exact=(check.test_type == TEST_TYPE_DIFF_FILE_CONTENT),
                fdiff_args=self.extra_args.fdiff_args )
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
            
        elif check.test_type in [TEST_TYPE_CHECK_EMPTY_FILES, TEST_TYPE_CHECK_NONEMPTY_FILES]:
            ref_file = os.path.join(self.test_work_path, check.data_file)
            sz = os.path.getsize(ref_file)
            if check.test_type == TEST_TYPE_CHECK_EMPTY_FILES:
                res = PASSED if sz == 0 else FAILED_NUTMEG_SPEC
            else:
                res = PASSED if sz != 0 else FAILED_NUTMEG_SPEC
            
        else:
            fatal_error("Unexpected check type " + TEST_TYPE_ID_TO_NAME[check.test_type])

        return res

    def run_and_validate_test(self, test_description: TestDescription) -> int:
                
        # 1) convert json file if needed
        if test_description.run_info.json_file: 
            res = self.run_dm_to_mdl_conversion(test_description.run_info.json_file)
            if res != PASSED:
                return res
            test_description.run_info.mdl_files = [ MAIN_MDL_FILE ]
        
        # 2) run mcell while capturing std and err output to different files
        #    non-zero exit code might be an expected result
        mcell_ec = self.run_mcell_for_nutmeg(test_description.run_info)

        # 3) run all checks
        for check in test_description.check_infos:
            res = self.run_check(check, mcell_ec)
            if res != PASSED:
                return res

        return PASSED

    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED

        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        # transform the result ito something more readable or keep as dictionary?
        parser = TestDescriptionParser(self.test_src_path)
        test_description = parser.parse_test_description()
        if test_description is None:
            return FAILED_NUTMEG_SPEC        

        res = self.run_and_validate_test(test_description)
         
        return res
