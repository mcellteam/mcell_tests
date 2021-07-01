"""
Copyright (C) 2019 by
The Salk Institute for Biological Studies and
Pittsburgh Supercomputing Center, Carnegie Mellon University

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
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
            self.mcell_path = opts.mcell_build_path_override
        else:
            self.mcell_path = os.path.join(MCELL_TOOLS_DIR, WORK_DIR_NAME, BUILD_DIR_MCELL)
        self.mcell_binary = os.path.join(self.mcell_path, MCELL_BINARY)
        self.postprocess_mcell3r_script = os.path.join(self.mcell_path, POSTPROCESS_MCELL3R_SCRIPT)
        self.pymcell_module = os.path.join(self.mcell_path, PYMCELL_PATH, PYMCELL_MODULE)
        self.pymcell4_lib = os.path.join(self.mcell_path, PYMCELL4_DIR, PYMCELL4_LIB)
            
        if opts.cellblender_build_path_override:
            self.cellblender_dir_path = opts.cellblender_build_path_override
        else:
            self.cellblender_dir_path = os.path.join(MCELL_TOOLS_DIR, WORK_DIR_NAME, BUILD_DIR_CELLBLENDER, REPO_NAME_CELLBLENDER)
            
        self.data_model_to_mdl_script = \
            os.path.join(self.cellblender_dir_path, DATA_MODEL_TO_MDL_DIR, DATA_MODEL_TO_MDL_SCRIPT)
            
        self.bngl_to_data_model_script = \
            os.path.join(self.cellblender_dir_path, BNG_DIR, BNGL_TO_DATA_MODEL_SCRIPT)

        if opts.bionetgen_path:
            self.bng2pl_script = os.path.join(opts.bionetgen_path, BNG2PL_SCRIPT)
        else:
            self.bng2pl_script = ''
            
        self.data_model_to_pymcell_binary = \
            os.path.join(self.mcell_path, DATA_MODEL_TO_PYMCELL_PATH, DATA_MODEL_TO_PYMCELL_BINARY)

        self.bng_analyzer_binary = \
            os.path.join(self.mcell_path, BNG_ANALYZER_DIR, BNG_ANALYZER_BINARY)
            
        self.work_path = os.path.join(THIS_DIR, '..', WORK_DIR_NAME)
        
        self.benchmark_script = os.path.join(self.work_path, 'run_benchmarks.sh')
        
        if opts.python_binary_override:
            self.python_binary = opts.python_binary_override
            if not os.path.exists(self.python_binary):
                fatal_error("Python binary from installed bundle was not found: '" + self.python_binary + "'.")
                
        else:
            self.python_binary = DEFAULT_PYTHON_BINARY         
            
        self.opts = opts    
            
    def __repr__(self) -> str:
        return \
            "Tool paths:\n" + \
            "  mcell_path: " + self.mcell_path + "\n" + \
            "  mcell_binary: " + self.mcell_binary + "\n" + \
            "  cellblender_dir: " + self.cellblender_dir_path + "\n" + \
            "  data_model_to_mdl_script: " + self.data_model_to_mdl_script + "\n" + \
            "  python_binary: " + self.python_binary
