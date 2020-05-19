#!/usr/bin/env bash

DIST_PATH=dist

# Execute preparation scripts for specific component.
prepare() {
  local component="$1"

  if [ -f ${DIST_PATH}/${component}/prepare_env.sh ]; then
    echo "Executing preparation script."
    cd ${DIST_PATH}/${component}
    source prepare_env.sh
    cd ../..
  fi
}

# Execute tear down scripts for specific component.
teardown() {
  local component="$1"

  if [ -f ${DIST_PATH}/${component}/teardown_env.sh ]; then
    echo "Executing teardown script."
    cd ${DIST_PATH}/${component}/
    bash teardown_env.sh
    cd ../..
  fi
}
