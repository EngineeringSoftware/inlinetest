#!/bin/bash
# test the project, with inline test plugin loaded but disabled
# this script is executed under the project directory root
# argument: 
# $1: path to conda.sh

conda_path=$1; shift
env_name=inline-testing

source ${conda_path}
conda activate $env_name

set -e
# only testing the examples we touched; there are hundreds of other examples in the repo, but not all of them have/pass the tests
pytest --inlinetest-disable sha1.py
