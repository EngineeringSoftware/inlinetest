#!/bin/bash
# test the project, with only inline tests
# this script is executed under the project directory root
# argument: 
# $1: not used
# $2: the path to inlinetest-1.0.jar

not_used=$1; shift
inline_test_path=$1; shift

set -e
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 8.0.302-open
sdk use java 8.0.302-open

pwd=$(pwd)
cd ./jadx-core/build/classes/java/main/
java -ea jadx/core/xmlgen/CommonBinaryParserTest
cd $pwd
