#!/bin/bash

# $1 - test script
# $2 - test dir
# $3 - work dir

if [ "`uname`" == "MSYS_NT-10.0-19042" ]; then 
    echo "TODO - Windows, skipped for now"
    exit 0
fi


mkdir -p $3
cd $3
python3 $1 $2/test_input.species > test_output.species || exit 1
diff --strip-trailing-cr test_output.species $2/reference_output.species
EC=$?
if [ $EC != 0 ]; then
  echo "ERROR: $1 - testing output differs from reference."
  exit 1
fi
exit 0
