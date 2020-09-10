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
This module contains definition of a bbase class used to run tests.
"""

import abc
import os
import sys
import shutil
import toml
import re
from typing import List, Dict

import data_output_diff

from test_settings import *
from test_utils import log_test_error, log_test_success, replace_in_file, find_in_file
from tool_paths import ToolPaths


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

VERBOSE_DIFF = False

ARGS_FILE = 'args.toml'

MCELL_ARGS_KEY = 'mcell'
FDIFF_ARGS_KEY = 'fdiff'
FDIFF_DATAMODEL_CONVERTER_ARGS_KEY = 'fdiff_datamodel_converter'


class ExtraArgs:
    def __init__(self, test_src_path: str):
        self.mcell_args = []
        self.fdiff_args = []
        # only for cases when the tester is TesterDatamodelConverter
        # rework needed if there will be more such cases, 
        # i.e. to make the argument system more general 
        self.fdiff_datamodel_converter_args = []  

        # parse args.toml if present        
        args_file_name = os.path.join(test_src_path, ARGS_FILE)
        if os.path.exists(args_file_name):
            top_dict = toml.load(args_file_name)
            if MCELL_ARGS_KEY in top_dict:
                args_str =  top_dict[MCELL_ARGS_KEY]
                self.mcell_args = args_str.split(' ')
            if FDIFF_ARGS_KEY in top_dict:
                args_str =  top_dict[FDIFF_ARGS_KEY]
                self.fdiff_args = args_str.split(' ')
            if FDIFF_DATAMODEL_CONVERTER_ARGS_KEY in top_dict:
                fdiff_datamodel_converter_args =  top_dict[FDIFF_DATAMODEL_CONVERTER_ARGS_KEY]
                self.fdiff_datamodel_converter_args = fdiff_datamodel_converter_args.split(' ')

def get_underscored(class_name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()


def get_tester_name(class_def):
    if class_def.__name__.startswith('Tester'):
        name = class_def.__name__[len('Tester'):]
    else:
        name = class_def.__name__
    return get_underscored(name) 


# TODO: maybe move check_preconditions and other things such as initialization 
# out, 
class TesterBase:
    def __init__(self, test_src_path: str, args: List[str], tool_paths: ToolPaths):
        
        self.mcell4_testing = False
        self.args = args
        if args:
            if args == ['mcell4']:
                self.mcell4_testing = True

        self.tester_name = get_tester_name(type(self)) 
        
        # paths to the binaries
        self.tool_paths = tool_paths

        # full path to the test        
        self.test_src_path = test_src_path
        
        # name of the specific test, e.g. 0000_1_mol_type_diffuse
        self.test_name = os.path.basename(self.test_src_path)

        # full path to the test set, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/tests/mdl/
        self.test_set_path = os.path.dirname(self.test_src_path)

        # full path to the test category, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/tests/
        self.test_category_path = os.path.dirname(self.test_set_path)

        # working directory for this specific test
        self.test_work_path = os.path.abspath(
            os.path.join(self.tool_paths.work_path,
                         self.tester_name, # set in parent
                         os.path.basename(self.test_category_path),
                         os.path.basename(self.test_set_path),
                         self.test_name
            )
        )

        self.extra_args = ExtraArgs(self.test_src_path)
        
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.mcell_binary):
            fatal_error("Could not find executable '" + tool_paths.mcell_binary + ".")

        data_output_diff.check_or_build_fdiff()
        
        # work dir, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/work         
        if not os.path.exists(tool_paths.work_path):
            os.mkdir(tool_paths.work_path)

    def should_be_skipped(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'skip')):
            log("SKIP : " + self.test_name)
            return True
        else:
            return False
            
    def is_known_fail(self) -> bool:
        # TODO: report this in a better way, should be reported as error when it starts to wok
        if os.path.exists(os.path.join(self.test_src_path, 'known_fail')):
            log("KNOWN FAIL : " + self.test_name)
            return True
        else:
            return False            

    def expected_wrong_ec(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'expected_wrong_ec')):
            log("EXPECTING WRONG EXIT CODE : " + self.test_name)
            return True
        else:
            return False

    def is_todo_test(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'todo')):
            log("TODO TEST : " + self.test_name)
            return True
        else:
            return False
    
    def clean_and_create_work_dir(self) -> None:
        if os.path.exists(self.test_work_path):
            # log("Erasing '" + self.test_name + "' in " + os.getcwd())
            shutil.rmtree(self.test_work_path)

        os.makedirs(self.test_work_path)
        os.chdir(self.test_work_path)
        assert self.test_work_path == os.getcwd()

    def check_reference(self, 
                        seed_dir: str, ref_dir_name: str, test_dir_name: str, exact_diff: bool, msg: str,
                        fdiff_args, required=False,
                        ) -> int:
        ref_path = os.path.join('..', self.test_src_path, ref_dir_name, seed_dir)
        if VERBOSE_DIFF:
            if os.path.exists(ref_path):
                log("DIFF DIR EXISTS: checking reference directory " + ref_path)
            else:
                log("DIFF NO REF DIR: checking reference directory " + ref_path)
                
        if not os.path.exists(ref_path):
            if required:
                log("Required reference data path " + ref_path + " was not found.")
                return FAILED_DIFF
            else:
                return PASSED
        
        res = data_output_diff.compare_data_output_directory(
            ref_path, 
            os.path.join(test_dir_name, seed_dir),
            exact_diff,
            fdiff_args)
        
        if res != PASSED:
            log_test_error(self.test_name, self.tester_name, msg)
        return res

    def check_reference_data(self, seed_dir: str, viz_ref_required=False, fdiff_args_override=None) -> int:
        
        if fdiff_args_override:
            fdiff_args = fdiff_args_override
        else:
            fdiff_args = self.extra_args.fdiff_args

        res = self.check_reference(
            seed_dir, get_ref_viz_data_dir(self.mcell4_testing), get_viz_data_dir(self.mcell4_testing), False, "Viz data diff failed.", fdiff_args, viz_ref_required)
        if res != PASSED:
            return res

        res = self.check_reference(
            seed_dir, get_ref_react_data_dir(self.mcell4_testing), get_react_data_dir(self.mcell4_testing), False, "React data diff failed.", fdiff_args)
        if res != PASSED:
            return res

        res = self.check_reference(
            '', REF_DYN_GEOM_DATA_DIR, DYN_GEOM_DATA_DIR, True, "Dynamic geometry data diff failed.", fdiff_args)
        if res != PASSED:
            return res

        res = self.check_reference(
            '', REF_MCELLR_GDAT_DATA_DIR, MCELLR_GDAT_DATA_DIR, True, "MCellR gdat data diff failed.", fdiff_args)
        if res != PASSED:
            return res
     
        if res == PASSED:
            log_test_success(self.test_name, self.tester_name)
        
        return res           

    # main_mdl_file - full path needst to be provided
    def run_mcell(self, mcell_args: List[str], main_mdl_file: str, timeout_sec=MCELL_TIMEOUT) -> int:
        cmd = [ self.tool_paths.mcell_binary ]
        cmd += mcell_args
        cmd += [ main_mdl_file ]
        cmd += self.extra_args.mcell_args

        # should we enable mcellr mode?
        mdlr_rules_file = os.path.join(self.test_work_path, MAIN_MDLR_RULES_FILE)
        if os.path.exists(mdlr_rules_file):
            cmd += [ '-r', mdlr_rules_file ]
        
        log_name = self.test_name+'.mcell.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=timeout_sec)
        if exit_code != 0:
            log_test_error(self.test_name, self.tester_name, "MCell failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED
    
    
    def postrocess_mcell3r(self, seed):
        cmd = [ self.tool_paths.python_binary, self.tool_paths.postprocess_mcell3r_script, str(seed), MAIN_MDLR_RULES_FILE ]
        log_name = self.test_name + '.postprocess_mcell3r.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            log_test_error(self.test_name, self.tester_name, "MCell3r postprocess failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED

         
    def run_dm_to_mdl_conversion(self, json_file_name: str, extra_arg: str = None) -> None:
        # the conversion python script is considered a separate utility, 
        # we run it through bash 
        cmd = [ 
            self.tool_paths.python_binary, self.tool_paths.data_model_to_mdl_script, 
            json_file_name, MAIN_MDL_FILE, '-fail-on-error' ]
        if extra_arg:
            cmd.append(extra_arg)    
        log_name = self.test_name+'.dm_to_mdl.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name)
        if exit_code != 0:
            log_test_error(self.test_name, self.tester_name, "Data model to mdl conversion failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_DM_TO_MDL_CONVERSION
        else:
            return PASSED

    def run_bngl_to_dm_conversion(self, bngl_file_name: str, extra_arg: str = None) -> None:
        # the conversion python script is considered a separate utility, 
        # we run it through bash 
        cmd = [ 
            self.tool_paths.python_binary, self.tool_paths.bngl_to_data_model_script, 
            bngl_file_name, 'data_model.json']
        if extra_arg:
            cmd.append(extra_arg)    
        log_name = self.test_name+'.bngl_to_dm.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name)
        if exit_code != 0:
            log_test_error(self.test_name, self.tester_name, "BGNL to mdl conversion failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_DM_TO_MDL_CONVERSION
        else:
            return PASSED
        
    def convert_bngl_to_mdl(self, only_last_viz_output=False):
        res = self.run_bngl_to_dm_conversion(os.path.join(self.test_src_path, 'test.bngl'))
        if res != PASSED:
            return res
        
        res = self.run_dm_to_mdl_conversion(os.path.join(self.test_work_path, 'data_model.json'))
        if res != PASSED:
            return res
        self.change_viz_output_to_ascii()
        if (only_last_viz_output):
            self.change_viz_output_to_output_only_last_it()
        return res       
        
    def change_viz_output_to_ascii(self):
        fname = os.path.join(self.test_work_path, 'Scene.viz_output.mdl')
        replace_in_file(fname, 'CELLBLENDER', 'ASCII')
        
    def change_viz_output_to_output_only_last_it(self):
        # get iterations from Scene.main.mdl
        main_fname = os.path.join(self.test_work_path, 'Scene.main.mdl')

        iters_line = find_in_file(main_fname, 'ITERATIONS')
        if iters_line:
            iters_str = iters_line.split()[2]
        else:
            print("Did not find ITERATIONS, could not update viz output to produce output on the last iteration")
            return
        
        # update ITERATION_NUMBERS
        viz_fname = os.path.join(self.test_work_path, 'Scene.viz_output.mdl')
        replace_in_file(
            viz_fname, 
            'ITERATION_NUMBERS {ALL_DATA @ ALL_ITERATIONS}', 
            'ITERATION_NUMBERS {ALL_DATA @ [[0 TO ' + iters_str + ' STEP ' + iters_str + ']]}'
        )
        
    @abc.abstractmethod        
    def test(self) -> int:
        pass  # derived methods return integer value PASSED, FAILED_MCELL, etc.
        
