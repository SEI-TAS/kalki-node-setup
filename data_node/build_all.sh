#!/bin/bash

# Include functions.
source ../build_functions.sh

# Clean dist
rm -r ${DIST_FOLDER}

# Copy configs to temp submodules.
copy_deployment_configs "$1"

# Build images and dist folders for all components.
build_image_lib "kalki-db"
build_and_dist "ovs-docker-server" "kalki-umbox-controller/ovs-docker-server"
build_and_dist "kalki-iot-interface"
