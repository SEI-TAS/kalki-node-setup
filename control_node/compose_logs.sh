#!/usr/bin/env bash

source ../run_functions.sh
MERGED_FILES=$(merge_docker_files "kalki-umbox-controller" "kalki-main-controller" "kalki-device-controller")
docker-compose ${MERGED_FILES} logs -f
