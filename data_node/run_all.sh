#!/usr/bin/env bash

source ../../kalki-repos/kalki-umbox-controller/ovs-docker-server/prepare_env.sh

export HOST_TZ=$(cat /etc/timezone)
docker-compose up -d -f ../../kalki-repos/kalki-iot-interface/docker-compose.yml \
                     -f ../../kalki-repos/kalki-umbox-controller/ovs-docker-server/docker-compose.yml
bash compose_logs.sh
