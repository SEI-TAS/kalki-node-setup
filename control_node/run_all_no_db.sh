#!/usr/bin/env bash

if [ ! -f run_functions.sh ]; then
  cp ../run_functions.sh .
fi

# Include functions.
source run_functions.sh

# Prepare envs for each component.
prepare "kalki-umbox-controller"
prepare "kalki-main-controller"
prepare "kalki-device-controller"

# Start them all in compose.
export HOST_TZ=$(cat /etc/timezone)
export CMD_PARAMS="$@"
docker-compose up -d -f docker-compose-no-db.yml --no-build

# Show logs.
bash compose_logs.sh
