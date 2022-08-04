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
