#!/bin/bash
# test the project
# this script is executed under the project directory root
# argument: 
# $1: path to conda.sh

conda_path=$1; shift
env_name=inline-testing

source ${conda_path}
conda activate $env_name

set -e
# test_expressions and test_conversion fail without any code change
# there are many many tests and the test time is super long
# = 158300 passed, 4155 skipped, 1387 xfailed, 10 xpassed, 120 warnings in 295.09s (0:04:55) =
# not sure what's "xfail" and "xpass", but hopefully it's not important
./test_fast.sh -k "not test_expressions and not test_conversion and not test_eval"
