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
# only testing the examples we touched; there are hundreds of other examples in the repo, but not all of them have/pass the tests
pytest sha1.py
