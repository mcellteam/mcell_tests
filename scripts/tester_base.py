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

from test_utils import ToolPaths

class TesterBase:
    def __init__(self, test_dir: str, tool_paths: ToolPaths):
        self.tool_paths = tool_paths

        # full path to the test        
        self.test_dir = test_dir
        
        # name of the specific test, e.g. 0000_1_mol_type_diffuse
        self.test_name = os.path.basename(self.test_dir)

        # full path to the test set, e.g. /nadata/cnl/home/ahusar/src/mcell_tests/tests_mdl/
        self.test_set_dir = os.path.dirname(self.test_dir)

        # full of the test set, e.g. tests_mdl
        self.test_set_name = os.path.basename(self.test_set_dir)

        
    @abc.abstractmethod        
    def test(self):
        pass # normally is an integer PASSED, FAILED_MCELL, ... returned
    