#!/usr/bin/env bash

BASE_PATH=../../kalki-repos/dn

source ${BASE_PATH}/kalki-umbox-controller/ovs-docker-server/prepare_env.sh

export HOST_TZ=$(cat /etc/timezone)
docker-compose up -d -f ${BASE_PATH}/kalki-iot-interface/docker-compose.yml \
                     -f ${BASE_PATH}/kalki-umbox-controller/ovs-docker-server/docker-compose.yml
bash compose_logs.sh
