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

def fatal_error(msg) -> None:
    log(msg)
    sys.exit(1)


def log_test_error(test_name, tester_class, msg) -> None:
    log("ERROR: " + test_name + " [" + tester_class + "]" + " - " + msg)


def log_test_success(test_name, tester_class) -> None:
    log("PASS : " + test_name + " [" + tester_class + "]")
    
    
def replace_in_file(fname, search_for, replace_with) -> None:
    lines = []
    with open(fname, "r") as infile:
        for line in infile:
            line = line.replace(search_for, replace_with)
            lines.append(line)
    with open(fname, "w") as outfile:
        for line in lines:
            outfile.write(line)
   
def find_in_file(fname, search_for) -> None:
    lines = []
    with open(fname, "r") as infile:
        for line in infile:
            if search_for in line:
                return line
    return ''
