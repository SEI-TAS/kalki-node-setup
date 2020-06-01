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

# Merge all component docker compose files to start them.
merge_docker_files() {
  local compose_files=""
  for component in "$@"; do
    compose_files="${compose_files} -f $DIST_PATH/$component/docker-compose.yml"
  done
  echo ${compose_files}
}

export_image() {
  local component="$1"
  local folder="$2"
  echo "Exporting image for component $component"
  docker save kalki/${component}:latest | gzip > ${folder}/${component}.tar.gz
}

import_image() {
  local component="$1"
  echo "Importing image for component $component"
  docker load < ${component}.tar.gz
}
