#!/bin/bash

# only cares about executing the inline tests, don't care about setting up env

inline_test_path=$1; shift
example=$1; shift

set -e
java -jar $inline_test_path --output_mode=new --assertion_style=assert --input_file=${example}.java --load_xml=false
src=${example}Test.java
if [[ -d ${example} ]]; then
        src="$src ${example}/*.java"
fi
javac -cp ${inline_test_path} $src
java -cp .:${inline_test_path}:${example} -ea ${example}Test
