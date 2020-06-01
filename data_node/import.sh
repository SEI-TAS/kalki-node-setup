#!/usr/bin/env bash

import_image() {
  local component="$1"
  local folder="$2"
  echo "Importing image for component $component"
  docker load < ${folder}/${component}.tar.gz
}

DIST_FOLDER=data_node_dist

echo "Extracting compressed output file..."
tar -zxvf data_node_dist.tar.gz

echo "Importing docker images..."
import_image "kalki-iot-interface" ${DIST_FOLDER}
import_image "ovs-docker-server" ${DIST_FOLDER}

echo "Finished"
