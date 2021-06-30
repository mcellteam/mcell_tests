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
This module contains definition of a base class used to run tests.
"""

import abc
import os
import sys
import shutil
import toml
import re
import glob
from typing import List, Dict

import data_output_diff

from test_settings import *
from test_utils import replace_in_file, find_in_file
from tool_paths import ToolPaths


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

VERBOSE_DIFF = False

ARGS_FILE = 'args.toml'

MCELL_ARGS_KEY = 'mcell'
FDIFF_ARGS_KEY = 'fdiff'
SEED_ARGS_KEY = 'seed'
FDIFF_DATAMODEL_CONVERTER_ARGS_KEY = 'fdiff_datamodel_converter'


class ExtraArgs:
    def __init__(self, test_src_path: str):
        self.mcell_args = []
        self.fdiff_args = []
        self.custom_seed_arg = None
        # only for cases when the tester is TesterDatamodelConverter
        # rework needed if there will be more such cases, 
        # i.e. to make the argument system more general 
        self.fdiff_datamodel_converter_args = []  

        # 32-bit model of MCell4
        self.mcell4_32 = False

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
            if SEED_ARGS_KEY in top_dict:
                seed_str =  top_dict[SEED_ARGS_KEY]
                self.custom_seed_arg = int(seed_str)
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
    def __init__(self, test_src_path: str, test_dir_suffix:str, args: List[str], tool_paths: ToolPaths):
        
        self.mcell4_testing = False
        self.args = args
        if args:
            if ARG_MCELL4 in args:
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
                         self.tester_name + test_dir_suffix, # tester_name is set in parent
                         os.path.basename(self.test_category_path),
                         os.path.basename(self.test_set_path),
                         self.test_name
            )
        )

        self.extra_args = ExtraArgs(self.test_src_path)
        
        self.extra_args.mcell4_32 = self.tool_paths.opts.mcell4_32_ref_data
        
        self.used_seed = None # set in run_* methods
        
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        if not os.path.exists(tool_paths.mcell_binary):
            fatal_error("Could not find executable '" + tool_paths.mcell_binary + ".")

        data_output_diff.check_or_build_fdiff()
        
        # work dir, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/work         
        if not os.path.exists(tool_paths.work_path):
            os.mkdir(tool_paths.work_path)

    def get_args_str(self):
        args_str = ''
        if self.args:
            args_str = ' - ' +  ','.join(self.args)
        return args_str

    def log_test_error(self, msg) -> None:
        log("ERROR: " + self.test_name + " [" + self.tester_name + self.get_args_str() + "]" + " - " + msg)

    def log_test_skip(self, custom_skip=None) -> None:
        skip = "SKIP" if custom_skip is None else custom_skip
        log(skip + " : " + self.test_name + " [" + self.tester_name + self.get_args_str() + "]")

    def log_test_todo(self, custom_todo=None) -> None:
        todo = "TODO TEST" if custom_todo is None else custom_todo
        log(todo + " : " + self.test_name + " [" + self.tester_name + self.get_args_str() + "]")
    
    def log_test_success(self) -> None:
        args_str = ''
        if self.args:
            args_str = ' - ' +  ','.join(self.args)
        log("PASS : " + self.test_name + " [" + self.tester_name + self.get_args_str() + "]")
        
    def should_be_skipped(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'skip')):
            self.log_test_skip()
            return True
        if os.path.exists(os.path.join(self.test_src_path, 'skip_debug')):
            # detection uses the parent directory of mcell
            mcell_path = os.path.basename(os.path.dirname(self.tool_paths.mcell_binary))
            if 'debug' in mcell_path:
                self.log_test_skip()
                return True
        if os.path.exists(os.path.join(self.test_src_path, 'skip_win')):
            if os.name == 'nt':
                log("SKIP WIN: " + self.test_name)
                return True
        if os.path.exists(os.path.join(self.test_src_path, 'skip_centos6')):
            if 'centos-6' in platform.platform():
                log("SKIP CENTOS6: " + self.test_name)
                return True
        if os.path.exists(os.path.join(self.test_src_path, 'skip_macos')):
            if 'Darwin' in platform.system():
                log("SKIP MACOS: " + self.test_name)
                return True
        
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
        
    def expected_wrong_ec_bng(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'expected_wrong_ec_bng')):
            return True
        else:
            return False        

    def is_todo_test(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'todo')):
            self.log_test_todo()
            return True
        else:
            return False
    
    def get_seed_dir(self):
        assert self.used_seed
        return 'seed_' + str(self.used_seed).zfill(5)
    
    def clean_and_create_work_dir(self) -> None:
        if os.path.exists(self.test_work_path):
            # log("Erasing '" + self.test_name + "' in " + os.getcwd())
            shutil.rmtree(self.test_work_path)

        os.makedirs(self.test_work_path)
        os.chdir(self.test_work_path)
        assert self.test_work_path == os.getcwd()

    def copy_all_extra_files_to_work_dir(self):
        for file in glob.glob(os.path.join(self.test_src_path, '*.bngl')):
            shutil.copy(
                file,
                self.test_work_path 
            )
        for file in glob.glob(os.path.join(self.test_src_path, '*.species')):
            shutil.copy(
                file,
                self.test_work_path 
            )
        for file in glob.glob(os.path.join(self.test_src_path, '*.dat')):
            shutil.copy(
                file,
                self.test_work_path 
            )
            
    # fdiff args are commandline arguments passed to fdiff, a single string representing a 
    # floating point value specifies tolerance
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
                return FAILED_REF_DATA_NOT_FOUND
            else:
                return PASSED
        
        res = data_output_diff.compare_data_output_directory(
            ref_path, 
            os.path.join(test_dir_name, seed_dir),
            exact_diff,
            fdiff_args)
        
        if res != PASSED:
            self.log_test_error(msg)
        return res
        
    def check_reference_data(self, viz_ref_required=False, fdiff_args_override=None) -> int:
        
        assert self.used_seed
        seed_dir = self.get_seed_dir()
        
        if fdiff_args_override:
            fdiff_args = fdiff_args_override
        else:
            fdiff_args = self.extra_args.fdiff_args

        res = self.check_reference(
            seed_dir, get_ref_viz_data_dir(self.mcell4_testing, self.extra_args.mcell4_32), get_viz_data_dir(self.mcell4_testing), False, "Viz data diff failed.", fdiff_args, viz_ref_required)
        if res != PASSED:
            return res

        res = self.check_reference(
            seed_dir, get_ref_react_data_dir(self.mcell4_testing, self.extra_args.mcell4_32), get_react_data_dir(self.mcell4_testing), True, "React data diff failed.", fdiff_args)
        if res != PASSED:
            return res

        if not self.mcell4_testing:
            res = self.check_reference(
                '', REF_DYN_GEOM_DATA_DIR, DYN_GEOM_DATA_DIR, True, "Dynamic geometry data diff failed.", fdiff_args)
            if res != PASSED:
                return res

        if not self.mcell4_testing:
            res = self.check_reference(
                '', REF_MCELLR_GDAT_DATA_DIR, MCELLR_GDAT_DATA_DIR, True, "MCellR gdat data diff failed.", fdiff_args)
            if res != PASSED:
                return res
     
        if res == PASSED:
            self.log_test_success()
        
        return res           

    def get_log_name(self, extension, seed = 1):
        if not seed or seed == 1:
            log_name = os.path.join(self.test_work_path, self.test_name+extension)  
        else:
            log_name = os.path.join(self.test_work_path, self.test_name + '_' + str(seed).zfill(5) + extension)  
        
        if os.name == 'nt': 
            if len(log_name) > MAX_WIN_PATH_LENGTH:
                log_name = os.path.join(self.test_work_path, 'l' + '.dm_to_mdl.log')
            if len(log_name) > MAX_WIN_PATH_LENGTH:
                print("Warning, path length is too long and will probably fail, error for " + log_name) 
        return log_name
        
    # main_mdl_file - full path needst to be provided
    def run_mcell(self, mcell_args: List[str], main_mdl_file: str, seed=1, timeout_sec=MCELL_TIMEOUT) -> int:
        cmd = [ self.tool_paths.mcell_binary ]
        cmd += mcell_args
        
        if self.extra_args.custom_seed_arg or seed != 1:
            # seed set as argument to this method has higher priority
            if seed != 1:
                self.used_seed = seed
            else:
                self.used_seed = self.extra_args.custom_seed_arg
        else:
            self.used_seed = 1
        cmd += ['-seed', str(self.used_seed)]
                
        cmd += [ main_mdl_file ]
        cmd += self.extra_args.mcell_args

        # should we enable mcellr mode?
        mdlr_rules_file = os.path.join(self.test_work_path, MAIN_MDLR_RULES_FILE)
        if os.path.exists(mdlr_rules_file):
            cmd += [ '-r', mdlr_rules_file ]
        
        if '-mcell4' in cmd:
            extension = '.mcell4.log'
        else:
            extension = '.mcell3.log'
        
        log_name = self.get_log_name(extension, seed)
            
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=timeout_sec)
        if exit_code != 0:
            self.log_test_error("MCell failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED
    
    
    def postrocess_mcell3r(self, seed=None):
        # seed argument has higher priority (used from validation scripts)
        # otherwise we will use the value used to run MCell 
        if seed:
            seed_to_convert = seed
        else:
            assert self.used_seed
            seed_to_convert = self.used_seed 
            
        cmd = [ self.tool_paths.python_binary, self.tool_paths.postprocess_mcell3r_script, str(seed_to_convert), MAIN_MDLR_RULES_FILE ]
        log_name = self.get_log_name('.postprocess_mcell3r.log', seed)
        
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            self.log_test_error("MCell3r postprocess failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
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
        log_name = self.get_log_name('.dm_to_mdl.log')
            
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name)
        if exit_code != 0:
            self.log_test_error("Data model to mdl conversion failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
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
            
        log_name = self.get_log_name('.bngl_to_dm.log')
                
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name)
        if exit_code != 0:
            self.log_test_error("BGNL to mdl conversion failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_DM_TO_MDL_CONVERSION
        else:
            return PASSED

    # erases the the react_data directory
    def run_mdl_to_dm_conversion(self, mcell_args: List[str], main_mdl_file: str):
        cmd = [ self.tool_paths.mcell_binary ]
        cmd += mcell_args
        cmd += [ main_mdl_file ]
        cmd += self.extra_args.mcell_args
        cmd += [ '-mdl2datamodel4' ]
        
        log_name = self.get_log_name('.mcell_mdl_to_dm.log')
        
        exit_code = run(cmd, cwd=self.test_work_path, verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            self.log_test_error("MCell state to data model conversion failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            # this might create file in the react_output directory, erase it
            # checks in comparisons
            shutil.rmtree(os.path.join(self.test_work_path, 'react_data'), ignore_errors=True)
            return PASSED
        
        
    def run_dm_to_pymcell_conversion(self, data_model_file: str, extra_args=[]):
        cmd = [ self.tool_paths.data_model_to_pymcell_binary, data_model_file ]
        cmd += extra_args
        
        prefix = ''
        prefix_file = os.path.join(self.test_src_path, 'mcell4_prefix')
        if os.path.exists(prefix_file):
            with open(prefix_file, 'r') as fin:
                prefix = fin.readline().strip()
                cmd += [ '-o', prefix ]
        
        log_name = self.get_log_name('.mcell_dm_to_pymcell.log')
        
        exit_code = run(cmd, cwd=self.test_work_path, verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            self.log_test_error("Data model to pymcell4 conversion failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            if prefix:
                # rename the main file because the rest of the system expects it to be called model.py
                shutil.move(os.path.join(self.test_work_path, prefix + '_model.py'), os.path.join(self.test_work_path, 'model.py'))
            
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
        
    def load_checkpoint_iters(self):
        iters_file_name = os.path.join(self.test_src_path, 'checkpoint_iters')
        
        if not os.path.exists(iters_file_name):
            return None
        
        res = []
        with open(iters_file_name, 'r') as f:
            for line in f:
                if line.strip():
                    res.append(line.strip())
        
        return res
        
    def run_finished(self, report_file):
        # simple grep
        with open(report_file, 'r') as f:
            for line in f:
                if 'FINISHED' in line:
                    return True
        
        return False
        
    @abc.abstractmethod        
    def test(self) -> int:
        pass  # derived methods return integer value PASSED, FAILED_MCELL, etc.
        
