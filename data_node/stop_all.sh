#!/usr/bin/env bash

DIST_PATH=dist

teardown() {
  local component="$1"

  # Execute prepartion scripts for specific component.
  if [ -f ${DIST_PATH}/${component}/teardown_env.sh ]; then
    echo "Executing preparation script."
    (cd ${DIST_PATH}/${component}/ && \
     bash teardown_env.sh)
  fi
}

# Merge all component docker compose files to start them.
merge_docker_files() {
  local compose_files=""
  for component in "$@"; do
    compose_files="${compose_files} -f $DIST_PATH/$component/docker-compose.yml"
  done
  echo compose_files
}

# Actual start of script.

teardown "kalki-iot-interface"
teardown "ovs-docker-server"

MERGED_FILES=$(merge_docker_files "kalki-iot-interface" "ovs-docker-server")
docker-compose "${MERGED_FILES}" down
