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

# First start kalki-postgres container separately, and wait for it.
(cd $DIST_PATH/kalki-db && bash run_postgres_container.sh)
bash wait_for_postgres.sh kalki-postgres

# Now start the rest
MERGED_FILES=$(merge_docker_files "kalki-umbox-controller" "kalki-main-controller" "kalki-device-controller")
docker-compose ${MERGED_FILES} up -d --no-build

# Show logs.
bash compose_logs.sh
