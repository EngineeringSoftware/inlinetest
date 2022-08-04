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
pytest -m "not selenium" --deselect=tests/unit/bokeh/command/subcommands/test_json__subcommands.py::test_no_script --deselect=tests/unit/bokeh/core/property/test_visual.py::Test_Image::test_transform_PIL[gif] tests/unit
