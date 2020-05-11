#!/bin/bash

BASE_PATH=../submodules

( \
  cd ${BASE_PATH} || exit && \
  (cd kalki-iot-interface && bash build_compose.sh ) && \
  (cd kalki-umbox-controller/ovs-docker-server && bash build_container.sh ) \
)

# Copy dist scripts to local temp dir.
rm -r dist

mkdir -p dist/ovs-docker-server
mkdir -p dist/ovs-docker-server/ovs-scripts
cp ${BASE_PATH}/kalki-umbox-controller/ovs-docker-server/*.sh dist/ovs-docker-server/
cp ${BASE_PATH}/kalki-umbox-controller/ovs-docker-server/ovs-scripts/*.sh dist/ovs-docker-server/ovs-scripts/
cp ${BASE_PATH}/kalki-umbox-controller/ovs-docker-server/docker-compose.yml dist/ovs-docker-server/

mkdir -p dist/kalki-iot-interface
cp ${BASE_PATH}/kalki-iot-interface/docker-compose.yml dist/kalki-iot-interface/
