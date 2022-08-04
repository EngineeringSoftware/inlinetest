#!/bin/bash

_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd ${_DIR}
rm -rf miniconda __pycache__ .pytest_cache .DS_Store
cd ../
zip -r userstudy.zip userstudy
