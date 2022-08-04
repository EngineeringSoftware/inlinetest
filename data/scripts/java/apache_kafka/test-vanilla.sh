#!/bin/bash
# test the project
# this script is executed under the project directory root
# argument: 
# $1: not used

not_used=$1; shift

set -e
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install gradle 7.3.3
sdk use gradle 7.3.3
sdk install java 8.0.302-open
sdk use java 8.0.302-open

# gradle --no-daemon --console=plain cleanTest unitTest -x :storage:unitTest
gradle --no-daemon --console=plain cleanTest :streams:examples:unitTest :streams:test-utils:unitTest
