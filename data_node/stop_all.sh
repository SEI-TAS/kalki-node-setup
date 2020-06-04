#!/usr/bin/env bash

# Include functions.
source run_functions.sh

# Teardown envs as needed.
teardown "kalki-iot-interface"
teardown "ovs-docker-server"

# Stop all components.
MERGED_FILES=$(merge_docker_files "kalki-iot-interface" "ovs-docker-server")
docker-compose ${MERGED_FILES} down
