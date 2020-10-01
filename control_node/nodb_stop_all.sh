#!/usr/bin/env bash

# Include functions.
source run_functions.sh

# Teardown envs as needed.
teardown "kalki-device-controller"
teardown "kalki-main-controller"
teardown "kalki-umbox-controller"

# Stop all components.
docker-compose -f nodb-docker-compose.yml down
