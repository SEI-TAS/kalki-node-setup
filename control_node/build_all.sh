#!/bin/bash

( \
  cd ../../kalki-repos/dn || exit && \
  (cd kalki-iot-interface && bash build_compose.sh ) && \
  (cd kalki-umbox-controller/ovs-docker-server && bash build_container.sh ) \
)
