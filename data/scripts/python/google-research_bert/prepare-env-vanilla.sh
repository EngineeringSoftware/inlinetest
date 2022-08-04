#!/bin/bash
# prepares a vanilla conda environment for the project (usually called "inline-testing")
# this script is executed under the project directory root
# argument: 
# $1: path to conda.sh

conda_path=$1; shift
env_name=inline-testing

set -e
source ${conda_path}
conda env remove --name $env_name
conda create --name $env_name python=3.6 pip -y
conda activate $env_name
pip install --upgrade pip
pip install tensorflow==1.11.0
pip install 'pytest>=7.0.0'
