#!/bin/bash

_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

function get_conda_path() {
        local conda_exe=$(which conda | xargs readlink -f)
        if [[ -z ${conda_exe} ]]; then
                echo "Fail to detect conda! Have you installed Anaconda/Miniconda?" 1>&2
                exit 1
        fi

        echo "$(dirname ${conda_exe})/../etc/profile.d/conda.sh"
}

function prepare_conda_env {
        ### Preparing the base environment "inline"
        local env_name=${1:-inline-testing}; shift
        local conda_path=$1; shift

        set -e
        if [[ -z ${conda_path} ]]; then
                conda_path=$(get_conda_path)
        fi
        echo ">>> Preparing conda environment \"${env_name}\", for cuda version: ${cuda_version}; conda at ${conda_path}"
        
        # Preparation
        source ${conda_path}
        conda env remove --name $env_name
        conda create --name $env_name python=3.9 pip -y
        conda activate $env_name
        
        # install inline test plugin
        ( cd ${_DIR}/../../../python
                pip install -e .
        )

        # install some other libraries required by import
        pip install pandas requests
}

prepare_conda_env "$@"
