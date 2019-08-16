/******************************************************************************
 *
 * Copyright (C) 2019 by
 * The Salk Institute for Biological Studies and
 * Pittsburgh Supercomputing Center, Carnegie Mellon University
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
 * USA.
 *
******************************************************************************/

/**
 * This is a simple tool that allows to diff two mcell viz_output files with
 * a given tolerance for floating-point computations.
 * Original implementation was in Python, but that one was too slow
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <stdexcept>      // std::invalid_argument
#include <iomanip>

using namespace std;

typedef float float_t;

const float_t EPS = 1e-10;
const int EXPECTED_NR_OF_VALUES = 7;


struct line_info {
  string name;
  float_t values[EXPECTED_NR_OF_VALUES];

  void clear() {
    name = "";
    memset(values, 0, EXPECTED_NR_OF_VALUES * sizeof(float_t));
  }
};


bool parse_line(const string& line, line_info& info) {
  info.clear();
  // name is first
  size_t pos1 = 0;
  size_t pos2 = line.find(' ');
  if (pos2 == string::npos) {
    // end of file?
    if (line == "") {
      return true;
    }
    else {
      return false;
    }
  }
  info.name = line.substr(pos1, pos2);

  string num;
  for (int i = 0; i < EXPECTED_NR_OF_VALUES; i++) {
    pos1 = pos2 + 1;
    pos2 = line.find(' ', pos1);

    if (i != EXPECTED_NR_OF_VALUES-1 && pos2 == string::npos) {
      return false;
    }

    try {
      info.values[i] = stof(line.substr(pos1, pos2));
    }
    catch (invalid_argument) {
      return false;
    }
  }

  // there shouldn't be anything more
  if (pos2 != string::npos) {
    return false;
  }

  return true;
}


string fdiff_streams(ifstream& ref, ifstream& test) {
  string ref_line, test_line;
  line_info ref_info, test_info;

  while (!ref.eof() && !test.eof()) {
    getline(ref, ref_line);
    getline(test, test_line);

    if (!parse_line(ref_line, ref_info)) {
      return "Could not read reference line";
    }
    if (!parse_line(test_line, test_info)) {
      return "Could not read test line";
    }

    if (ref_info.name != test_info.name) {
      return "Different molecule name";
    }

    for (int i = 0; i < EXPECTED_NR_OF_VALUES; i++) {
      if (fabs(ref_info.values[i] - test_info.values[i]) > EPS) {
        stringstream ss;
        ss << "Values " << setprecision(10) << ref_info.values[i] << " and " << setprecision(10) << test_info.values[i] << " differ";
        return ss.str();
      }
    }
  }

  if (ref.eof() != test.eof()) {
    return "Different number of lines";
  }
  return "";
}


int main(const int argc, const char* argv[]) {
  if (argc != 3) {
    cerr << "Expecting reference and testing output file names.\n";
    exit(1);
  }
  const char* fname_ref = argv[1];
  const char* fname_test = argv[2];

  ifstream ref(fname_ref);
  if (!ref.is_open()) {
    cerr << "Could not open reference file " << fname_ref << ".\n";
    return 1;
  }

  ifstream test(fname_test);
  if (!test.is_open()) {
    cerr << "Could not open test file " << fname_test << ".\n";
    ref.close();
    exit(1);
  }

  string res = fdiff_streams(ref, test);

  ref.close();
  test.close();

  if (res != "") {
    cerr << "Difference between " << fname_ref << " and " << fname_test << ": " << res << ".\n";
    exit(1);
  }

  return 0;
}

