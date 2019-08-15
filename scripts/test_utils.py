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


# this class contains all paths that are used during testing
# and also derived paths 
class ToolPaths:
    def __init__(self):
        self.mcell_dir = ''
        self.mcell_binary = ''

        self.celblender_dir = ''
        
        self.work_dir = ''

    def __init__(self, install_dirs):
        if REPO_NAME_MCELL in install_dirs:
            self.mcell_dir = install_dirs[REPO_NAME_MCELL]
        else:
            self.mcell_dir = os.path.join(MCELL_TOOLS_DIR, WORK_DIR_NAME, BUILD_DIR_MCELL)
        self.mcell_binary = os.path.join(self.mcell_dir, MCELL_BINARY)
            
        if REPO_NAME_CELLBLENDER in install_dirs:
            self.celblender_dir = install_dirs[REPO_NAME_CELLBLENDER]
        else:
            self.celblender_dir = os.path.join(MCELL_TOOLS_DIR, WORK_DIR_NAME, BUILD_DIR_CELLBLENDER)
            
    def dump(self):
        log("Tool paths:")
        log("  mcell_dir: " + mcell_dir)
        log("  mcell_binary: " + mcell_binary)
        log("  celblender_dir: " + celblender_dir)


def fatal_error(msg):
    print(msg)
    sys.exit(1)


def report_test_error(test_name, msg):
    print('ERROR: ' + test_name + ' - ' + msg)
    # terminate for now
    # fatal_error('Ending after first error')


def report_test_success(test_name):
    print('PASS : ' + test_name)
    

