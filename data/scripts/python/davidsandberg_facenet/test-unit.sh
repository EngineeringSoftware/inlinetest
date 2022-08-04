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
PYTHONPATH=./src:./src/models:./src/align pytest -k "not train_test" --inlinetest-disable test
