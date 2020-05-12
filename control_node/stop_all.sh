#!/usr/bin/env bash

# Include functions.
source ../run_functions.sh

# Teardown envs as needed.
teardown "kalki-device-controller"
teardown "kalki-main-controller"
teardown "kalki-umbox-controller"
teardown "kalki-db"

# Stop all components.
MERGED_FILES=$(merge_docker_files "kalki-db" "kalki-umbox-controller" "kalki-main-controller" "kalki-device-controller")
docker-compose ${MERGED_FILES} down
