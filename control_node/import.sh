#!/usr/bin/env bash

import_image() {
  local component="$1"
  local folder="$2"
  echo "Importing image for component $component"
  docker load < ${folder}/${component}.tar.gz
}

DIST_FOLDER=control_node_dist

echo "Extracting compressed output file..."
tar -zxvf control_node_dist.tar.gz

echo "Importing docker images..."
import_image "kalki-postgres" ${DIST_FOLDER}
import_image "kalki-umbox-controller" ${DIST_FOLDER}
import_image "kalki-main-controller" ${DIST_FOLDER}
import_image "kalki-device-controller" ${DIST_FOLDER}

echo "Finished"
