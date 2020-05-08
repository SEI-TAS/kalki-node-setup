#!/usr/bin/env bash

BASE_PATH=../../kalki-repos/dn

(cd ${BASE_PATH}/kalki-umbox-controller/ovs-docker-server/ && source teardown_env.sh)

docker-compose -f ${BASE_PATH}/kalki-iot-interface/docker-compose.yml \
               -f ${BASE_PATH}/kalki-umbox-controller/ovs-docker-server/docker-compose.yml \
               down
