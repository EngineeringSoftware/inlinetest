#!/bin/bash
# test the project
# this script is executed under the project directory root
# argument: 
# $1: not used

not_used=$1; shift

set -e
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install maven 3.8.3
sdk use maven 3.8.3
sdk install java 8.0.302-open
sdk use java 8.0.302-open

MVN_SKIPS="-Djacoco.skip -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dfindbugs.skip -Dwarbucks.skip -Dmodernizer.skip -Dimpsort.skip -Dpmd.skip -Dxjc.skip"

mvn test $MVN_SKIPS
