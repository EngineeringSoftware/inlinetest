#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Script needs 1 arguments: python file"
    echo "Example: bash parallel_tests.sh a.py"
else
    script_dir=$( cd $( dirname $0 ) && pwd )
    logs_dir="$script_dir/logs"
    test_file="$script_dir/${1}"

    mkdir -p $logs_dir

    pip uninstall -y pytest-xdist

    echo "Running non-parallel..."
    ( time pytest $test_file ) &> "$logs_dir/non-parallel"
    echo "Finished non-parallel"

    pip install pytest-xdist

    echo "Running parallel..."
    ( time pytest -n auto $test_file ) &> "$logs_dir/parallel"
    echo "Finished non-parallel"

    echo "Logs in: $logs_dir"
fi