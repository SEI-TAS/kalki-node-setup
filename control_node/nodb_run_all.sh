#!/usr/bin/env bash

# Include functions.
cp ../run_functions.sh .
source run_functions.sh

# Prepare envs for each component.
prepare "kalki-umbox-controller"
prepare "kalki-main-controller"
prepare "kalki-device-controller"

# Copy kalki-umboxcontroller tests in case they are needed.
cp dist/kalki-umbox-controller/tests/* ./tests/

# Start them all in compose.
export HOST_TZ=$(cat /etc/timezone)
export CMD_PARAMS="$@"
docker-compose -f nodb-docker-compose.yml up -d --no-build

# Show logs.
bash nodb_compose_logs.sh
