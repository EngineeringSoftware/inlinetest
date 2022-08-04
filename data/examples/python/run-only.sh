#!/bin/bash

conda_path=$1; shift
example=$1; shift
env_name=inline-testing

source ${conda_path}
conda activate $env_name

pytest -m "inline" $example.py
