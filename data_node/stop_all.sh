#!/usr/bin/env bash

# Include functions.
source ../run_functions.sh

# Teardown envs as needed.
teardown "kalki-iot-interface"
teardown "ovs-docker-server"

# Stop all components.
docker-compose down
