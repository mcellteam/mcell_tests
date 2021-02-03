#!/bin/bash

# $1 - bng_analyzer
# $2 - test dir
# $3 - work dir

if [ "`uname`" != "MSYS_NT-10.0-19042" ]; then 
    echo "TODO - Windows, skipped for now"
    exit 0
fi

mkdir -p $3
cd $3
$1 $2/in.CaMKII.species > out.CaMKII.species || exit 1
diff out.CaMKII.species $2/ref.CaMKII.species
EC=$?
if [ $EC != 0 ]; then
  echo "ERROR: bng_analyzer - testing output differs from reference."
  exit 1
fi
exit 0
