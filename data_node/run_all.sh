#!/usr/bin/env bash

(cd dist/ovs-docker-server/ && source prepare_env.sh)

export HOST_TZ=$(cat /etc/timezone)
docker-compose -f dist/kalki-iot-interface/docker-compose.yml \
               -f dist/ovs-docker-server/docker-compose.yml \
               up -d
bash compose_logs.sh
