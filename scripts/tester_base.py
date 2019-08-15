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
import test_utils

class TesterBase:
    def __init__(self, test_dir: str, tool_paths: ToolPaths):
        self.test_dir = test_dir
        self.tool_paths = tool_paths
        
    @abc.abstractmethod        
    def test(self):
        pass
    