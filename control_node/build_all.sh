#!/bin/bash

# Include functions.
source ../build_functions.sh

# Clean dist
sudo rm -r ${DIST_FOLDER}

# Check if we got the deployment.
if [ -z "$1" ]; then
  echo "No deployment provided."
else
  # Copy configs to temp submodules.
  copy_deployment_configs "$1" control_node
fi

# Build images and dist folders for all components.
build_image_lib "kalki-db"
build_and_dist "kalki-db"
build_and_dist "kalki-umbox-controller"
build_and_dist "kalki-main-controller"
build_and_dist "kalki-device-controller"
