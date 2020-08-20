#!/usr/bin/env bash

if [ ! -f run_functions.sh ]; then
  cp ../run_functions.sh .
fi

# Include functions.
source run_functions.sh

# Clear DB volume if requested
if [ "$1" == "--reset_db" ] || [ "$1" == "test" ]; then
  echo "DB reset requested, removing existing DB volume if any..."
  docker volume rm kalki-pgdata
fi

# Prepare envs for each component.
prepare "kalki-db"
prepare "kalki-umbox-controller"
prepare "kalki-main-controller"
prepare "kalki-device-controller"

# Start them all in compose.
export HOST_TZ=$(cat /etc/timezone)
export CMD_PARAMS="$@"
docker-compose up -d --no-build

# Show logs.
bash compose_logs.sh
