#!/bin/bash
# prepares a conda environment for the project, with inline test installed (usually called "inline-testing")
# this script is executed under the project directory root
# argument: 
# $1: path to conda.sh
# $2: the path to inlinetest/python (the place to do pip install)

conda_path=$1; shift
inline_test_path=$1; shift
env_name=inline-testing

set -e
source ${conda_path}
conda env remove --name $env_name
conda create --name $env_name python=3.9 pip -y
conda activate $env_name
conda install libgcc
ICU_VERSION=66.1 pip install -r requirements.txt
( cd $inline_test_path && pip install -e . )
