#!/bin/bash

update_repo() {
  local repo_name="$1"
  (cd ${repo_name} && git checkout dev && git pull)
}

(git submodule update --init && \
 cd ../submodules && \
 update_repo "kalki-iot-interface" && \
 update_repo "kalki-umbox-controller" )
