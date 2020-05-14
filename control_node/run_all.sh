#!/usr/bin/env bash

# Include functions.
source ../run_functions.sh

# Prepare envs for each component.
prepare "kalki-db"
prepare "kalki-umbox-controller"
prepare "kalki-main-controller"
prepare "kalki-device-controller"

# Start them all in compose.
export HOST_TZ=$(cat /etc/timezone)

# First start kalki-postgres container
MERGED_FILES=$(merge_docker_files "kalki-db")
docker-compose ${MERGED_FILES} up -d --no-build

# Wait for the DB container to be up.
bash wait_for_postgres.sh kalki-postgres

# Now start the rest
MERGED_FILES=$(merge_docker_files "kalki-umbox-controller" "kalki-main-controller" "kalki-device-controller")
docker-compose ${MERGED_FILES} up -d --no-build

# Show logs.
bash compose_logs.sh
