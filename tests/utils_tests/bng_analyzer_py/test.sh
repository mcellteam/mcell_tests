#!/bin/bash

# $1 - test script
# $2 - test dir
# $3 - work dir

mkdir -p $3
cd $3
python3 $1 $2/test_input.dat > test_output.txt || exit 1
diff test_output.txt $2/reference_output.txt
EC=$?
if [ $EC != 0 ]; then
  echo "ERROR: bng_analyzer_py - testing output differs from reference."
  exit 1
fi
exit 0
