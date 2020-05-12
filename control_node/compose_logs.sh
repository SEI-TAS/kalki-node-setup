#!/usr/bin/env bash

BASE_PATH=../submodules
MERGED_FILES=$(merge_docker_files "kalki-db" "kalki-umbox-controller" "kalki-main-controller" "kalki-device-controller")
docker-compose ${MERGED_FILES} logs -f
