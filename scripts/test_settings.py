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
This module contains diverse constants used while testing.
"""
import os
import sys

WORK_DIR_NAME = 'work'

TEST_MCELL4 = False

BUILD_OPTS_USE_LTO = False  # higher performnce but slower build

MAIN_MDL_FILE = 'Scene.main.mdl'
MAIN_MDLR_RULES_FILE = 'Scene.mdlr_rules.xml'

MCELL_BINARY = 'mcell'

PYTHON_BINARY = 'python'
DATA_MODEL_TO_MDL_DIR = 'mdl'
DATA_MODEL_TO_MDL_SCRIPT = 'data_model_to_mdl.py'


MCELL_TIMEOUT=600

PASSED = 1
SKIPPED = 2

FAILED_DM_TO_MDL_CONVERSION = 10
FAILED_MCELL = 11
FAILED_DIFF = 12
FAILED_NUTMEG_SPEC = 13

RESULT_NAMES = {
 PASSED:'PASSED',
 SKIPPED:'SKIPPED',
 FAILED_DM_TO_MDL_CONVERSION:'FAILED_DM_TO_MDL_CONVERSION',
 FAILED_MCELL:'FAILED_MCELL',
 FAILED_DIFF:'FAILED_DIFF',
 FAILED_NUTMEG_SPEC:'FAILED_NUTMEG_SPEC'
}

MCELL_ARGS = []

if TEST_MCELL4:
    MCELL_ARGS.append('-mcell4')
    
    VIZ_DATA_DIR = os.path.join('4.', 'viz_data')
    REF_VIZ_DATA_DIR = 'ref_viz_data_4'

    REACT_DATA_DIR = os.path.join('4.', 'react_data')
    REF_REACT_DATA_DIR = 'ref_react_data_4'

    REF_NUTMEG_DATA_DIR = 'ref_data_4'
else:
    VIZ_DATA_DIR = 'viz_data'
    REF_VIZ_DATA_DIR = 'ref_viz_data_3'
    
    REACT_DATA_DIR = 'react_data'
    REF_REACT_DATA_DIR = 'ref_react_data_3'
    
    DYN_GEOM_DATA_DIR = 'dynamic_geometry'
    REF_DYN_GEOM_DATA_DIR = 'ref_dynamic_geometry_3'
    
    MCELLR_GDAT_DATA_DIR = '.'
    REF_MCELLR_GDAT_DATA_DIR = 'ref_mcellr_gdat_3'

    REF_NUTMEG_DATA_DIR = 'ref_data_3'
    


TEST_SETTINGS_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MCELL_TOOLS_DIR = os.path.realpath(os.path.join(TEST_SETTINGS_BASE_DIR, '..', '..', 'mcell_tools'))
sys.path.append(os.path.join(MCELL_TOOLS_DIR, 'scripts'))

from build_settings import \
    REPO_NAME_MCELL, REPO_NAME_CELLBLENDER, \
    WORK_DIR_NAME, \
    BUILD_DIR_MCELL, BUILD_DIR_CELLBLENDER
