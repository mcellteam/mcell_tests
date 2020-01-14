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

from typing import Dict
from test_settings import *
THIS_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(THIS_DIR, '..', '..', 'mcell_tools', 'scripts'))
from utils import *


# this class contains all paths that are used during testing
# and also derived paths 
class ToolPaths:
    def __init__(self, opts): 
        if opts.mcell_build_path_override:
            self.mcell_dir_path = opts.mcell_build_path_override
        else:
            self.mcell_dir_path = os.path.join(MCELL_TOOLS_DIR, WORK_DIR_NAME, BUILD_DIR_MCELL)
        self.mcell_binary = os.path.join(self.mcell_dir_path, MCELL_BINARY)
        self.pymcell_module = os.path.join(self.mcell_dir_path, PYMCELL_DIR, PYMCELL_MODULE)
            
        if opts.cellblender_build_path_override:
            self.cellblender_dir_path = opts.cellblender_build_path_override
        else:
            self.cellblender_dir_path = os.path.join(MCELL_TOOLS_DIR, WORK_DIR_NAME, BUILD_DIR_CELLBLENDER, REPO_NAME_CELLBLENDER)
            
        self.data_model_to_mdl_script = \
            os.path.join(self.cellblender_dir_path, DATA_MODEL_TO_MDL_DIR, DATA_MODEL_TO_MDL_SCRIPT)
            
        self.work_path = os.path.join(THIS_DIR, '..', WORK_DIR_NAME)
        
        if opts.python_binary_override:
            self.python_binary = opts.python_binary_override
            if not os.path.exists(self.python_binary):
                fatal_error("Python binary from installed bundle was not found: '" + self.python_binary + "'.")
                
        else:
            self.python_binary = DEFAULT_PYTHON_BINARY            
            
    def __repr__(self) -> str:
        return \
            "Tool paths:\n" + \
            "  mcell_dir: " + self.mcell_dir_path + "\n" + \
            "  mcell_binary: " + self.mcell_binary + "\n" + \
            "  cellblender_dir: " + self.cellblender_dir_path + "\n" + \
            "  data_model_to_mdl_script: " + self.data_model_to_mdl_script + "\n" + \
            "  python_binary: " + self.python_binary


def fatal_error(msg) -> None:
    log(msg)
    sys.exit(1)


def log_test_error(test_name, msg) -> None:
    log("ERROR: " + test_name + " - " + msg)


def log_test_success(test_name) -> None:
    log("PASS : " + test_name)
    
    
def replace_in_file(fname, search_for, replace_with) -> None:
    lines = []
    with open(fname, "r") as infile:
        for line in infile:
            line = line.replace(search_for, replace_with)
            lines.append(line)
    with open(fname, "w") as outfile:
        for line in lines:
            outfile.write(line)
   
    
    

