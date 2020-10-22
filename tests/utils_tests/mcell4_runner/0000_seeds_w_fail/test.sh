#!/bin/bash

MCELL_BUILD_DIR=$1
MCELL_TESTS_DIR=$2

rm -f log.tmp

export MCELL_PATH=$MCELL_BUILD_DIR; \
    python $MCELL_BUILD_DIR/utils/mcell4_runner.py \
    $MCELL_TESTS_DIR/tests/utils_tests/mcell4_runner/0000_seeds_w_fail/test.py \
    -s 1:3:1 > log.tmp

# expected to fail
EC1=$?

grep "1/3 runs failed" log.tmp 
EC2=$?
    
if [ "$EC1" != "0" -a "$EC2" == "0" ]; then
    exit 0
else
    exit 1
fi
     