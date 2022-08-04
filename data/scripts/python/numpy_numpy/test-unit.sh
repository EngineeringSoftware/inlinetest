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
# "test_new_policy" spawns new pytest processes without properly setting up the required environment (with inline test plugin), so we have to skip it
pytest -k "not test_new_policy" --inlinetest-disable --deselect=numpy/lib/tests/test_function_base.py::TestLerp::test_linear_interpolation_formula_symmetric .
