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
pytest --deselect=tests/test_format.py::test_source_is_formatted[src/black/trans.py] .
