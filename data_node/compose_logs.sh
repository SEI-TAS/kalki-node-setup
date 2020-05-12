#!/usr/bin/env bash

BASE_PATH=../submodules
MERGED_FILES=$(merge_docker_files "kalki-iot-interface" "ovs-docker-server")
docker-compose ${MERGED_FILES} logs -f
