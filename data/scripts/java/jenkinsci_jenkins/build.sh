#!/bin/bash
# build the project
# this script is executed under the project directory root
# argument: 
# $1: not used

set -e
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install maven 3.8.3
sdk use maven 3.8.3
sdk install java 8.0.302-open
sdk use java 8.0.302-open

MVN_SKIPS="-Djacoco.skip -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dfindbugs.skip -Dwarbucks.skip -Dmodernizer.skip -Dimpsort.skip -Dpmd.skip -Dxjc.skip -Dspotless.check.skip=true -Dlicense.disableCheck"

mvn test-compile $MVN_SKIPS
