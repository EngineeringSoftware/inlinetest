#!/bin/bash
# test the project, with inline test plugin loaded but disabled
# this script is executed under the project directory root
# argument: 
# $1: not used
# $2: the path to inlinetest-1.0.jar

not_used=$1; shift
inline_test_path=$1; shift

# use test-vanilla.sh
_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
${_DIR}/test-vanilla.sh $not_used $inline_test_path
