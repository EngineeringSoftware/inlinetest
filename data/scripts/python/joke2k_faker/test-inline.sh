#!/bin/bash
# test the project, with only inline tests
# this script is executed under the project directory root
# argument: 
# $1: path to conda.sh

conda_path=$1; shift
env_name=inline-testing

source ${conda_path}
conda activate $env_name

set -e
pytest -m "inline" faker/providers/internet/__init__.py
