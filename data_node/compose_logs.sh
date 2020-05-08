#!/usr/bin/env bash

BASE_PATH=../../kalki-repos/dn
docker-compose -f ${BASE_PATH}/kalki-iot-interface/docker-compose.yml \
               -f ${BASE_PATH}/kalki-umbox-controller/ovs-docker-server/docker-compose.yml \
               logs -f