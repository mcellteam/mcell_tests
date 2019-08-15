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


WORK_DIR_NAME = 'work'

BUILD_OPTS_USE_LTO = False  # higher performnce but slower build

MCELL_BINARY = 'mcell'

MCELL_ARGS = ['-mcell4', '-seed', '1']

VIZ_OUTPUT_DIR = os.path.join('4.', 'viz_data')
REF_VIZ_OUTPUT_DIR = 'ref_viz_data'
MAIN_MDL_FILE = 'Scene.main.mdl'
SEED_DIR = 'seed_00001'

PASSED = 1
FAILED_MCELL = 2
FAILED_DIFF = 3
SKIPPED = 4

RESULT_NAMES = {
 PASSED:'PASSED',
 FAILED_MCELL:'FAILED_MCELL',
 FAILED_DIFF:'FAILED_DIFF',
 SKIPPED:'SKIPPED'
}




TEST_SETTINGS_BASE_DIR = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
MCELL_TOOLS_DIR = os.path.join(TEST_SETTINGS_BASE_DIR, '..', 'mcell_tools')
sys.path.append(os.path.join(TEST_SETTINGS_BASE_DIR, '..', 'mcell_tools', 'scripts'))

from build_settings import \
    REPO_NAME_MCELL, REPO_NAME_CELLBLENDER, \
    WORK_DIR_NAME, \
    BUILD_DIR_MCELL, BUILD_DIR_CELLBLENDER