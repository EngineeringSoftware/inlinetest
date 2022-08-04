#!/bin/bash
# build the project
# this script is executed under the project directory root
# argument: 
# $1: not used

set -e
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install gradle 7.4.1
sdk use gradle 7.4.1
sdk install java 8.0.302-open
sdk use java 8.0.302-open

gradle --no-daemon --console=plain jar
