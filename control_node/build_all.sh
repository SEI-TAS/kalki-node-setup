#!/bin/bash

# Include functions.
source ../build_functions.sh

# Clean dist
rm -r $DIST_FOLDER

# Build images and dist folders for all components.
build_image_lib "kalki-db"
build_and_dist "kalki-db" "kalki-db"
build_and_dist "kalki-umbox-controller" "kalki-umbox-controller"
build_and_dist "kalki-main-controller" "kalki-main-controller"
build_and_dist "kalki-device-controller" "kalki-device-controller"
