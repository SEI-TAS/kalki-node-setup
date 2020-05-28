#!/usr/bin/env bash

# Include functions.
source ../run_functions.sh

# Prepare envs for each component.
prepare "kalki-iot-interface"
prepare "ovs-docker-server"

# Start them all in compose.
export HOST_TZ=$(cat /etc/timezone)
docker-compose up -d --no-build

# Show logs.
bash compose_logs.sh
