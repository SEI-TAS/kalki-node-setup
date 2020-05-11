#!/bin/bash

DIST_FOLDER="$PWD/dist"
BASE_PATH=../submodules

build_and_dist() {
  local component="$1"
  local component_folder="$2"
  local dist_folder="$3"

  # Create images.
  (cd ${BASE_PATH}/${component_folder} && bash build_compose.sh )

  # Copy docker-compose configs.
  mkdir -p dist/${component}
  cp ${BASE_PATH}/${component_folder}/docker-compose.yml ${dist_folder}/${component}/

  # Execute dist scripts for specific component.
  if [ -f ${BASE_PATH}/${component_folder}/create_dist.sh ]; then
    echo "Executing dist script."
    (cd ${BASE_PATH}/${component_folder}/ && \
     bash create_dist.sh "${dist_folder}/${component}")
  fi
}

# Copy dist scripts to local temp dir.
rm -r dist

build_and_dist "ovs-docker-server" "kalki-umbox-controller/ovs-docker-server" $DIST_FOLDER
build_and_dist "kalki-iot-interface" "kalki-iot-interface" $DIST_FOLDER
