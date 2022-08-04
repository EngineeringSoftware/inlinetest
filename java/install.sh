#!/bin/bash
_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

set -e

[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 8.0.302-open
sdk use java 8.0.302-open
sdk install maven 3.8.3
sdk use maven 3.8.3

( cd ${_DIR}
  mvn package
  mvn install
)
