#!/bin/bash
# test the project
# this script is executed under the project directory root
# argument: 
# $1: not used

not_used=$1; shift

set -e
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install gradle 7.4.1
sdk use gradle 7.4.1
sdk install java 8.0.302-open
sdk use java 8.0.302-open

# print test output to stdout
sed -Ei 's/test \{$/test { afterSuite { desc, result -> if (!desc.parent) { def output = "${result.testCount} tests completed, ${result.successfulTestCount} passed, ${result.failedTestCount} failed, ${result.skippedTestCount} skipped"; println(output)}}/g' build.gradle
gradle --no-daemon --console=plain cleanTest test
