#!/bin/bash

# $1 - mesh_utils_test
# $2 - test dir (with connectivity/ and reports/)
# $3 - work dir

mkdir -p $3
cd $3
$1 $2 > out.txt 2>&1
EC=$?
cat out.txt
if [ $EC != 0 ]; then
  echo "ERROR: mesh_utils_test - results differ from the expected ones, see out.txt."
  exit 1
fi
exit 0
