#!/bin/bash
# build the project; usually just no-op for python projects
# this script is executed under the project directory root
# argument: 
# $1: path to conda.sh

conda_path=$1; shift
env_name=inline-testing

source ${conda_path}
conda activate $env_name

bokeh sampledata
