#!/bin/bash
# build the project; usually just no-op for python projects
# this script is executed under the project directory root
# argument: 
# $1: path to conda.sh

conda_path=$1; shift
env_name=inline-testing

source ${conda_path}
conda activate $env_name

# run tests once to download data; it is ok for this to fail
PYTHONPATH=./src:./src/models:./src/align pytest test
echo "ok to fail"
