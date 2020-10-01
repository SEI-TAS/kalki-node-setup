#!/usr/bin/env bash

# Include functions.
cp ../run_functions.sh .
source run_functions.sh

# Prepare envs for each component.
prepare "kalki-iot-interface"
prepare "ovs-docker-server"

# Start them all in compose.
MERGED_FILES=$(merge_docker_files "kalki-iot-interface" "ovs-docker-server")
export HOST_TZ=$(cat /etc/timezone)
docker-compose ${MERGED_FILES} up -d --no-build

# Show logs.
bash compose_logs.sh
