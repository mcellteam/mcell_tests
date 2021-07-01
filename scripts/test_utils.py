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

def fatal_error(msg) -> None:
    log(msg)
    sys.exit(1)


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
