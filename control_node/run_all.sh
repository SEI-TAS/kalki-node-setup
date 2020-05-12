#!/usr/bin/env bash

# Include functions.
source ../run_functions.sh

# Prepare envs for each component.
prepare "kalki-db"
prepare "kalki-umbox-controller"
prepare "kalki-main-controller"
prepare "kalki-device-controller"

# Start them all in compose.
MERGED_FILES=$(merge_docker_files "kalki-db" "kalki-umbox-controller" "kalki-main-controller" "kalki-device-controller")
export HOST_TZ=$(cat /etc/timezone)
docker-compose ${MERGED_FILES} up -d --no-build

# Show logs.
bash compose_logs.sh
