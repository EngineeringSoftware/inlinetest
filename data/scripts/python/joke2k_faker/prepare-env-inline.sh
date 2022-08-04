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
pip install -e .
echo "coverage>=5.2
freezegun<0.4
pytest>=7.0.0
random2>=1.0.1
ukpostcodeparser>=1.1.1
validators>=0.13.0
sphinx>=2.4,<3.0
Pillow" > requirements.txt
pip install -r requirements.txt
( cd $inline_test_path && pip install -e . )
