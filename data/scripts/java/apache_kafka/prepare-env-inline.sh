#!/bin/bash
# prepares a runtime environment for the project, with inline test installed; usually nothing to do for java
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

java -jar $inline_test_path --output_mode=new --assertion_style=assert --input_file=./streams/src/main/java/org/apache/kafka/streams/state/internals/Murmur3.java
