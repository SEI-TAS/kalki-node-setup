#!/usr/bin/env bash

# Include functions.
source run_functions.sh

# Teardown envs as needed.
teardown "kalki-device-controller"
teardown "kalki-main-controller"
teardown "kalki-umbox-controller"
teardown "kalki-db"

# Stop all components.
docker-compose down
