#!/usr/bin/env bash

source run_functions.sh
MERGED_FILES=$(merge_docker_files "kalki-iot-interface" "ovs-docker-server")
docker-compose ${MERGED_FILES} logs -f
