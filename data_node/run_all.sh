#!/usr/bin/env bash

DIST_PATH=dist

# Execute preparation scripts for specific component.
prepare() {
  local component="$1"

  if [ -f ${DIST_PATH}/${component}/prepare_env.sh ]; then
    echo "Executing preparation script."
    (cd ${DIST_PATH}/${component}/ && \
     source prepare_env.sh)
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

# Actual start of script.

prepare "kalki-iot-interface"
prepare "ovs-docker-server"

MERGED_FILES=$(merge_docker_files "kalki-iot-interface" "ovs-docker-server")
export HOST_TZ=$(cat /etc/timezone)
docker-compose "${MERGED_FILES}" up -d --no-build

bash compose_logs.sh
